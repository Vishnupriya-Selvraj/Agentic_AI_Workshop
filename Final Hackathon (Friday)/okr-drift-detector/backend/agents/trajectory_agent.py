from utils.rag_utils import GeminiRAGUtils
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class TrajectoryMapperAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def map_trajectory(self, okr_data: Dict[str, Any], quarterly_goal: str) -> str:
        """Map student's goal trajectory relative to quarterly goal across cycles"""
        
        # Get context from all pillars for comprehensive analysis
        all_contexts = []
        for okr in okr_data.get("okrs", []):
            pillar = okr.get("pillar", "CLT")
            objective = okr.get("title", "")
            
            context = self.rag_utils.query_pillar_knowledge(pillar, objective, k=2)
            all_contexts.extend(context)
        
        # Create a serializable copy of the data
        serializable_data = []
        for okr in okr_data.get("okrs", []):
            okr_copy = okr.copy()
            if "submittedOn" in okr_copy and okr_copy["submittedOn"] is not None:
                if isinstance(okr_copy["submittedOn"], datetime):
                    okr_copy["submittedOn"] = okr_copy["submittedOn"].isoformat()
                elif isinstance(okr_copy["submittedOn"], dict) and "$date" in okr_copy["submittedOn"]:
                    # Handle MongoDB date format
                    okr_copy["submittedOn"] = okr_copy["submittedOn"]["$date"]
            serializable_data.append(okr_copy)
        
        prompt = f"""
        Analyze the student's OKR progression  in relation to their quarterly goal: {quarterly_goal} across cycles and identify their trajectory.
        
        OKR History: {json.dumps(serializable_data, indent=2)}
        
        Consider the 5 OKR Pillars:
        - CLT: Center For Learning and Teaching (PrepInsta courses, GenAI, Product Management)
        - CFC: Center for Creativity (Hackathons, BMC videos, GenAI projects)
        - SCD: Skill & Career Development (LeetCode, Mock exams, Competitive programming)
        - IIPC: Industry Institute Patnership Cell (LinkedIn networking, Article writing)
        - SRI: Social Responsibility Initiative (Community engagement, Design thinking activities)
        
        Analyze:
        1. Primary focus areas and their evolution
        2. Skill progression patterns across pillars
        3. Career direction alignment and coherence
        4. Cross-pillar connections and synergies
        5. Depth vs breadth of skill development
        
        Focus on:
        1. How each OKR contributes to {quarterly_goal}
        2. The logical progression toward {quarterly_goal}
        3. Any missing elements needed for {quarterly_goal}
        
        Provide a trajectory summary specifically about progress toward {quarterly_goal}
        """
        
        trajectory_summary = await self.rag_utils.generate_with_context(prompt, all_contexts)
        return trajectory_summary