import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

class GeminiRAGUtils:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize ChromaDB
        self.chroma_client = chromadb.PersistentClient(
            path=os.getenv("CHROMA_PERSIST_DIRECTORY")
        )
        
        # Use Gemini embeddings 
        try:
            self.embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=os.getenv("GEMINI_API_KEY")
            )
        except:
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        self.setup_collections()
    
    def setup_collections(self):
        """Initialize ChromaDB collections for 5 pillars"""
        self.collections = {}
        for pillar in ["CLT", "CFC", "SCD", "IIPC", "SRI"]:
            self.collections[pillar] = self.chroma_client.get_or_create_collection(
                name=f"okr_{pillar.lower()}",
                embedding_function=self.embedding_function
            )
    
    async def fetch_and_store_pillar_data(self):
        """fetch web data for each pillar and store in ChromaDB"""
        
        # CLT Pillar - Learning resources
        clt_data = [
            {
                "content": "GenAI courses on PrepInsta platform focusing on practical AI applications and project-based learning",
                "metadata": {"pillar": "CLT", "type": "course", "platform": "PrepInsta", "domain": "GenAI"}
            },
            {
                "content": "Product Management certification from EdX covering user research, product strategy, and market analysis",
                "metadata": {"pillar": "CLT", "type": "course", "platform": "EdX", "domain": "Product Management"}
            },
            {
                "content": "Innovation and emerging technology courses covering blockchain, IoT, AR/VR, and quantum computing",
                "metadata": {"pillar": "CLT", "type": "course", "domain": "Innovation"}
            }
        ]
        
        # CFC Pillar - Hackathons and startup data
        cfc_data = await self.fetch_yc_companies()
        cfc_data.extend([
            {
                "content": "DevPost hackathons for team-based development projects with 3-5 members focusing on real-world problems",
                "metadata": {"pillar": "CFC", "type": "hackathon", "platform": "DevPost"}
            },
            {
                "content": "Unstop competitions and hackathons for skill development and industry exposure",
                "metadata": {"pillar": "CFC", "type": "hackathon", "platform": "Unstop"}
            }
        ])
        
        # SCD Pillar - Skill development resources
        scd_data = [
            {
                "content": "LeetCode problem solving for competitive programming and interview preparation",
                "metadata": {"pillar": "SCD", "type": "practice", "platform": "LeetCode"}
            },
            {
                "content": "Mock competitive exams for government positions including SSB and UPSC preparation",
                "metadata": {"pillar": "SCD", "type": "exam", "category": "Government"}
            },
            {
                "content": "SAT test preparation for academic excellence and international opportunities",
                "metadata": {"pillar": "SCD", "type": "exam", "category": "Academic"}
            }
        ]
        
        # IIPC Pillar - Industry connections
        iipc_data = [
            {
                "content": "LinkedIn networking with SNS15 Mango BiG7 professionals for industry insights",
                "metadata": {"pillar": "IIPC", "type": "networking", "category": "SNS15"}
            },
            {
                "content": "Connect with YCombinator startup founders and employees for startup ecosystem understanding",
                "metadata": {"pillar": "IIPC", "type": "networking", "category": "Startups"}
            },
            {
                "content": "Article writing on LinkedIn using hashtags #snsinstitutions #snsdesignthinkers #designthinking",
                "metadata": {"pillar": "IIPC", "type": "content", "platform": "LinkedIn"}
            }
        ]
        
        # SRI Pillar - Social responsibility
        sri_data = [
            {
                "content": "Design Thinking engagement activities with previous schools/colleges for community impact",
                "metadata": {"pillar": "SRI", "type": "community", "method": "Design Thinking"}
            },
            {
                "content": "Team-based social impact projects with 3-5 members focusing on local community problems",
                "metadata": {"pillar": "SRI", "type": "project", "team_size": "3-5"}
            }
        ]
        
        # Store data in respective collections
        pillar_data_map = {
            "CLT": clt_data,
            "CFC": cfc_data,
            "SCD": scd_data,
            "IIPC": iipc_data,
            "SRI": sri_data
        }
        
        for pillar, data in pillar_data_map.items():
            if data:
                documents = [item["content"] for item in data]
                metadatas = [item["metadata"] for item in data]
                ids = [f"{pillar}_{i}" for i in range(len(documents))]
                
                self.collections[pillar].add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
    
    async def fetch_yc_companies(self) -> List[Dict]:
        """fetch Y Combinator companies for CFC pillar"""
        companies_data = [
            {
                "content": "OpenAI - AI research and deployment company focusing on safe artificial general intelligence",
                "metadata": {"pillar": "CFC", "type": "company", "source": "YCombinator", "domain": "AI"}
            },
            {
                "content": "Stripe - Payment processing platform enabling online commerce for businesses worldwide",
                "metadata": {"pillar": "CFC", "type": "company", "source": "YCombinator", "domain": "FinTech"}
            },
            {
                "content": "Airbnb - Home sharing platform revolutionizing travel and accommodation industry",
                "metadata": {"pillar": "CFC", "type": "company", "source": "YCombinator", "domain": "Marketplace"}
            },
            {
                "content": "Dropbox - File storage and sharing platform for personal and business use",
                "metadata": {"pillar": "CFC", "type": "company", "source": "YCombinator", "domain": "Enterprise"}
            }
        ]
        return companies_data
    
    def query_pillar_knowledge(self, pillar: str, query: str, k: int = 5) -> List[Dict]:
        """Query specific pillar knowledge base"""
        if pillar not in self.collections:
            return []
        
        results = self.collections[pillar].query(
            query_texts=[query],
            n_results=k
        )
        
        return [
            {
                "content": doc,
                "metadata": meta
            }
            for doc, meta in zip(results['documents'][0], results['metadatas'][0])
        ]
    
    async def generate_with_context(self, prompt: str, context: List[Dict] = None) -> str:
        """Generate response using Gemini with RAG context"""
        if context:
            context_text = "\n".join([
                f"Context: {item['content']}\nMetadata: {item['metadata']}"
                for item in context
            ])
            full_prompt = f"Context Information:\n{context_text}\n\nQuery: {prompt}"
        else:
            full_prompt = prompt
        
        response = await self.model.generate_content_async(full_prompt)
        return response.text