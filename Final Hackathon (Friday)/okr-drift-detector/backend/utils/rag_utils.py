import google.generativeai as genai
import chromadb
from chromadb.utils import embedding_functions
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from typing import Optional

class GeminiRAGUtils:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize ChromaDB with auto-recovery
        self.chroma_path = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
        self._initialize_chroma_client()
        
        os.environ["CHROMA_GOOGLE_GENAI_API_KEY"] = api_key
        try:
            self.embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction()
        except Exception as e:
            print(f"⚠️ Using default embeddings - {str(e)}")
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        self.setup_collections()

    def _initialize_chroma_client(self, retries=3):
        """Initialize Chroma client with auto-recovery"""
        for attempt in range(retries):
            try:
                if not os.path.exists(self.chroma_path):
                    os.makedirs(self.chroma_path)
                
                self.chroma_client = chromadb.PersistentClient(path=self.chroma_path)
                # Test connection
                self.chroma_client.heartbeat()
                return
            except Exception as e:
                print(f"⚠️ ChromaDB init attempt {attempt+1} failed: {str(e)}")
                if attempt == retries - 1:
                    raise RuntimeError(f"Failed to initialize ChromaDB after {retries} attempts")
                
                # Clean up and retry
                import shutil
                if os.path.exists(self.chroma_path):
                    shutil.rmtree(self.chroma_path)
                os.makedirs(self.chroma_path)
                time.sleep(1)
        
        # Configure embeddings
        os.environ["CHROMA_GOOGLE_GENAI_API_KEY"] = api_key
        try:
            self.embedding_function = embedding_functions.GoogleGenerativeAiEmbeddingFunction()
        except Exception as e:
            print(f"⚠️ Using default embeddings - {str(e)}")
            self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        self.setup_collections()

    def _reinitialize_chroma(self, path: str):
        """Handle ChromaDB initialization errors by recreating the directory"""
        import shutil
        try:
            # Remove the problematic directory
            if os.path.exists(path):
                shutil.rmtree(path)
            # Create new client
            self.chroma_client = chromadb.PersistentClient(path=path)
            print("✅ Successfully reinitialized ChromaDB storage")
        except Exception as e:
            print(f"❌ Failed to reinitialize ChromaDB: {str(e)}")
            raise RuntimeError("Failed to initialize ChromaDB storage")

    def setup_collections(self):
        """Initialize collections with auto-recovery"""
        self.collections = {}
        self._collections_to_populate = []
        for pillar in ["CLT", "CFC", "SCD", "IIPC", "SRI"]:
            collection_name = f"okr_{pillar.lower()}"
            try:
                # Try existing collection first
                self.collections[pillar] = self.chroma_client.get_collection(collection_name)
            except Exception as e:
                print(f"⚠️ Collection {collection_name} not found, creating new: {str(e)}")
                try:
                    self.collections[pillar] = self.chroma_client.get_or_create_collection(
                        name=collection_name,
                        embedding_function=self.embedding_function
                    )
                    # Mark for population if empty
                    if self.collections[pillar].count() == 0:
                        self._collections_to_populate.append(pillar)
                except Exception as e:
                    print(f"❌ Failed to create collection {collection_name}: {str(e)}")
                    raise

    async def populate_collections_if_needed(self):
        """Populate collections that are empty after setup_collections"""
        if hasattr(self, '_collections_to_populate') and self._collections_to_populate:
            await self.fetch_and_store_pillar_data()

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
    
    async def generate_with_context(self, prompt: str, context: List[Dict] = None) -> Optional[str]:
        """Generate response using Gemini with RAG context"""
        try:
            if context:
                context_text = "\n".join([
                    f"Context: {item['content']}\nMetadata: {item['metadata']}"
                    for item in context
                ])
                full_prompt = f"Context Information:\n{context_text}\n\nQuery: {prompt}"
            else:
                full_prompt = prompt
            
            response = await self.model.generate_content_async(full_prompt)
            
            if not response or not response.text:
                print("Gemini returned empty response")
                return "No response generated"
                
            return response.text
        except Exception as e:
            print(f"Error generating content: {str(e)}")
            return f"Error generating response: {str(e)}"
        