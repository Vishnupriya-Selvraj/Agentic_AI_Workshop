from utils.rag_utils import GeminiRAGUtils
import json
from typing import Dict, Any, List, Optional

class PatternClassifierAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def classify_patterns(self, drift_report: Dict[str, Any], trajectory: str, quarterly_goal: str)  -> str:
        """Classify behavioral patterns in OKR changes"""
        
        # Get context for pattern recognition
        context = self.rag_utils.query_pillar_knowledge(
            "CLT", f"learning behavior patterns for {quarterly_goal}", k=3
         )
        
        prompt = f"""
         Analyze the student's behavioral pattern in relation to their quarterly goal: {quarterly_goal}
         
         Drift Report: {json.dumps(drift_report, indent=2)}
         Trajectory: {trajectory}
         
         Focus your analysis on:
         1. How well their activities align with {quarterly_goal}
         2. Whether their progress shows coherent development toward {quarterly_goal}
         3. Any deviations that might hinder achieving {quarterly_goal}
         
         Provide pattern classification specifically in context of {quarterly_goal}
         
      Use the following behavioral patterns as a reference:  
        Common OKR Behavioral Patterns:
        
        1. **Shiny Object Syndrome** - Frequent switches to trending topics without completion
           - Characteristics: Abandons previous goals for new trends, lack of follow-through
           
        2. **Healthy Exploration Phase** - Strategic experimentation across domains
           - Characteristics: Tries different areas but maintains some coherence
           
        3. **Iterative Refinement** - Gradual focus narrowing with consistent improvement
           - Characteristics: Progressive depth building, connected skill development
           
        4. **Strategic Pivot** - Deliberate direction changes based on learning
           - Characteristics: Clear reasoning for changes, builds on previous experience
           
        5. **Scattered Approach** - Lack of clear direction or strategy
           - Characteristics: Random goal selection, no apparent progression logic
           
        6. **Depth Building** - Consistent skill deepening in chosen areas
           - Characteristics: Advanced learning in specific domains, expertise development
           
        7. **Multi-Pillar Integration** - Effective connection across OKR pillars
           - Characteristics: Uses CLT learning in CFC projects, connects IIPC with other pillars
        
        Analyze the pattern and provide:
        1. Primary pattern classification
        2. Evidence from the data supporting this classification
        3. Any secondary patterns observed
        4. Overall assessment of goal coherence
        
        Format as a detailed pattern analysis (3-4 sentences).
        """
        
        pattern_analysis = await self.rag_utils.generate_with_context(prompt, context)
        return pattern_analysis