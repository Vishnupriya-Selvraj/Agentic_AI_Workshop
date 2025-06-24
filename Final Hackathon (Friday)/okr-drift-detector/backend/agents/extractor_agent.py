from typing import Dict, List, Any
from models.okr_model import okr_collection, OKRData, OKRPillar
from utils.rag_utils import GeminiRAGUtils
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

class OKRExtractorAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def extract_past_okrs(self, student_id: str, cycles: int = 3) -> Dict[str, Any]:
        """Extract OKRs from the last N cycles using RAG for context"""
        
        # Query MongoDB for student's OKR history
        cursor = okr_collection.find(
            {"student_id": student_id}
        ).sort("date_created", -1).limit(cycles * 5)  # Assuming max 5 OKRs per cycle
        
        okrs = await cursor.to_list(length=None)
        
        if not okrs:
            
            okrs = await self._generate_sample_okrs(student_id)
        
        # Use RAG to enrich OKR context
        enriched_okrs = []
        for okr in okrs:
            pillar = okr.get('pillar', 'CLT')
            
            # Query relevant pillar knowledge
            context = self.rag_utils.query_pillar_knowledge(
                pillar, 
                okr.get('objective', ''),
                k=3
            )
            
            # Enrich with context
            okr_data = {
                "cycle": okr.get('cycle'),
                "pillar": pillar,
                "objective": okr.get('objective'),
                "key_results": okr.get('key_results', []),
                "completion_status": okr.get('completion_status', 0),
                "metadata": okr.get('metadata', {}),
                "context": context
            }
            enriched_okrs.append(okr_data)
        
        return {"okrs": enriched_okrs}
    
    async def _generate_sample_okrs(self, student_id: str) -> List[Dict]:
        """Generate sample OKRs based on 5-pillar framework"""
        sample_okrs = [
            {
                "student_id": student_id,
                "cycle": "2024-Q1",
                "pillar": "CLT",
                "objective": "Complete 10+ hours GenAI course on PrepInsta and build AI project",
                "key_results": [
                    "Complete GenAI fundamentals course (10+ hours)",
                    "Build chatbot using LangChain",
                    "Write technical blog about GenAI learning"
                ],
                "completion_status": 0.8,
                "date_created": datetime.now() - timedelta(days=90),
                "metadata": {"platform": "PrepInsta", "course_type": "GenAI", "hours": 12}
            },
            {
                "student_id": student_id,
                "cycle": "2024-Q2",
                "pillar": "CFC",
                "objective": "Participate in DevPost hackathon and create BMC video",
                "key_results": [
                    "Join DevPost hackathon with team of 4",
                    "Create Business Model Canvas video for YC company",
                    "Present GenAI-based solution"
                ],
                "completion_status": 0.6,
                "date_created": datetime.now() - timedelta(days=60),
                "metadata": {"hackathon": "DevPost", "team_size": 4, "yc_company": "OpenAI"}
            },
            {
                "student_id": student_id,
                "cycle": "2024-Q3",
                "pillar": "SCD",
                "objective": "Solve 30+ LeetCode problems and take mock competitive exam",
                "key_results": [
                    "Solve minimum 30 new LeetCode problems",
                    "Take 1 mock SSB exam",
                    "Achieve 80%+ accuracy in problem solving"
                ],
                "completion_status": 0.9,
                "date_created": datetime.now() - timedelta(days=30),
                "metadata": {"platform": "LeetCode", "problems_solved": 35, "exam_type": "SSB"}
            }
        ]
        
        # Store sample OKRs in MongoDB
        await okr_collection.insert_many(sample_okrs)
        return sample_okrs