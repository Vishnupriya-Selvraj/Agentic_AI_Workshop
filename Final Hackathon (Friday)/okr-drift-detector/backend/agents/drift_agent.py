from utils.rag_utils import GeminiRAGUtils
import json
from typing import Dict, Any, List, Optional

class DriftDetectorAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def detect_drift(self, trajectory_summary: str, okr_data: Dict[str, Any]) -> Dict[str, Any]:
        """Detect goal drift using RAG for context"""
        
        # Query knowledge base for typical progression patterns
        context_queries = [
            "typical career progression patterns in technology",
            "coherent skill development pathways",
            "common goal drift patterns in students"
        ]
        
        all_contexts = []
        for query in context_queries:
            # Query across all pillars for comprehensive context
            for pillar in ["CLT", "CFC", "SCD", "IIPC", "SRI"]:
                context = self.rag_utils.query_pillar_knowledge(pillar, query, k=2)
                all_contexts.extend(context)
        
        prompt = f"""
        Analyze the student's OKR progression for goal drift patterns.
        
        Trajectory Summary: {trajectory_summary}
        OKR Data: {json.dumps(okr_data, indent=2)}
        
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
        
        Rate drift severity (Low/Medium/High) based on:
        - Low: Minor exploration, mostly coherent progression
        - Medium: Some scattered focus, partial alignment issues
        - High: Major inconsistencies, no clear direction
        
        Return as JSON with: {{"drift_level": "", "flagged_transitions": [], "reasoning": ""}}
        
        Each flagged_transition should include: {{"from": "", "to": "", "reason": ""}}
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