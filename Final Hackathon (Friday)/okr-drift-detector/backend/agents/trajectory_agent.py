from utils.rag_utils import GeminiRAGUtils
import json
from typing import Dict, Any, List, Optional

class TrajectoryMapperAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def map_trajectory(self, okr_data: Dict[str, Any]) -> str:
        """Map student's goal trajectory across cycles"""
        
        # Get context from all pillars for comprehensive analysis
        all_contexts = []
        for okr in okr_data.get("okrs", []):
            pillar = okr.get("pillar", "CLT")
            objective = okr.get("objective", "")
            
            context = self.rag_utils.query_pillar_knowledge(pillar, objective, k=2)
            all_contexts.extend(context)
        
        prompt = f"""
        Analyze the student's OKR progression across cycles and identify their trajectory.
        
        OKR History: {json.dumps(okr_data, indent=2)}
        
        Consider the 5 OKR Pillars:
        - CLT: Continuous Learning & Training (PrepInsta courses, GenAI, Product Management)
        - CFC: Create, Fund & Commercialize (Hackathons, BMC videos, GenAI projects)
        - SCD: Skill & Competency Development (LeetCode, Mock exams, Competitive programming)
        - IIPC: Industry Integration & Professional Connect (LinkedIn networking, Article writing)
        - SRI: Social Responsibility & Impact (Community engagement, Design thinking activities)
        
        Analyze:
        1. Primary focus areas and their evolution
        2. Skill progression patterns across pillars
        3. Career direction alignment and coherence
        4. Cross-pillar connections and synergies
        5. Depth vs breadth of skill development
        
        Provide a concise trajectory summary (2-3 sentences) that captures the student's goal progression pattern.
        """
        
        trajectory_summary = await self.rag_utils.generate_with_context(prompt, all_contexts)
        return trajectory_summary