from utils.rag_utils import GeminiRAGUtils
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

class DriftDetectorAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def detect_drift(self, trajectory_summary: str, okr_data: Dict[str, Any], quarterly_goal: str) -> Dict[str, Any]:
        """Detect goal drift relative to quarterly goal using RAG for context"""
        
        # Query knowledge base for typical progression patterns
        context_queries = [
            "typical student progression patterns in 5-pillar framework",
            "coherent skill development pathways in OKR system",
            "common goal drift patterns in student OKRs"
        ]
        
        all_contexts = []
        for query in context_queries:
            # Query across all pillars for comprehensive context
            for pillar in ["CLT", "CFC", "SCD", "IIPC", "SRI"]:
                context = self.rag_utils.query_pillar_knowledge(pillar, query, k=2)
                all_contexts.extend(context)
        
        # Create a serializable version of the data
        serializable_data = self._make_serializable(okr_data)
        
        prompt = f"""
        Analyze the student's OKR progression for goal drift patterns specifically in context of: {quarterly_goal}.
        
        Trajectory Summary: {trajectory_summary}
        OKR Data: {json.dumps(serializable_data, indent=2)}
        
        5-Pillar Framework Context:
        - CLT: Should show progressive learning (basic → advanced courses)
        - CFC: Should build from participation → creation → commercialization
        - SCD: Should demonstrate consistent skill building
        - IIPC: Should show growing professional network and thought leadership
        - SRI: Should demonstrate sustained community engagement
        
        Detect and analyze:
        1. Significant detours from logical progression within pillars
        2. Inconsistent pillar focus without clear strategic rationale
        3. Abandoned learning paths or incomplete skill development
        4. Conflicting objectives that don't build on each other
        5. Lack of cross-pillar synergy (e.g., not connecting CLT learning with CFC projects)
        
        For each detected drift, provide:
        - The specific transition that shows drift
        - The reason it's considered drift
        - Suggested corrective actions
        
        Rate drift severity (Low/Medium/High) based on:
        - Low: Minor exploration, mostly coherent progression
        - Medium: Some scattered focus, partial alignment issues
        - High: Major inconsistencies, no clear direction
        
        Identify:
        1. Activities that don't contribute to {quarterly_goal}
        2. Missing elements needed for {quarterly_goal}
        3. Any detours from the path to {quarterly_goal}
        
        Return analysis focused on {quarterly_goal} achievement
        
        Return as JSON with: {{"drift_level": "", "flagged_transitions": [], "reasoning": ""}}
        
        Each flagged_transition should include: {{"from": "", "to": "", "reason": "", "suggested_action": ""}}
        """
        
        response = await self.rag_utils.generate_with_context(prompt, all_contexts)
        
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_str = response[json_start:json_end]
                return json.loads(json_str)
        except:
            pass
        
        return {
            "drift_level": "Medium", 
            "flagged_transitions": [], 
            "reasoning": "Analysis completed but parsing failed"
        }

    def _make_serializable(self, data: Any) -> Any:
        """Recursively convert datetime objects to strings"""
        if isinstance(data, dict):
            return {k: self._make_serializable(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._make_serializable(item) for item in data]
        elif isinstance(data, datetime):
            return data.isoformat()
        elif hasattr(data, '__dict__'):
            return self._make_serializable(data.__dict__)
        return data