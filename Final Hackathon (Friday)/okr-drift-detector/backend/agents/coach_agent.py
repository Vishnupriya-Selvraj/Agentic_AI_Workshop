from utils.rag_utils import GeminiRAGUtils
import json
from typing import Dict, Any, List, Optional

class CoachingAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def generate_coaching(self, pattern: str, drift_report: Dict[str, Any], trajectory: str) -> List[str]:
        """Generate personalized coaching recommendations"""
        
        # Get context from all pillars for comprehensive coaching
        coaching_contexts = []
        for pillar in ["CLT", "CFC", "SCD", "IIPC", "SRI"]:
            context = self.rag_utils.query_pillar_knowledge(
                pillar, f"best practices recommendations {pillar}", k=2
            )
            coaching_contexts.extend(context)
        
        prompt = f"""
        Generate specific, actionable coaching recommendations based on the student's pattern and drift analysis.
        
        Pattern Classification: {pattern}
        Drift Report: {json.dumps(drift_report, indent=2)}
        Trajectory: {trajectory}
        
        5 Pillar Framework Guidelines:
        
        **CLT (Continuous Learning & Training):**
        - Monthly: 10+ hours on PrepInsta/EdX (GenAI, Product Management, Innovation)
        - Focus on structured, progressive learning paths
        - Connect learning to practical applications
        
        **CFC (Create, Fund & Commercialize):**
        - Monthly: DevPost/Unstop hackathons (3-5 member teams)
        - Monthly: BMC videos of YC/Unicorn companies
        - Quarterly: GenAI projects using Design Thinking
        - Limit problems to YC startup or Unicorn company variations
        
        **SCD (Skill & Competency Development):**
        - Monthly: Mock competitive exams (SSB/UPSC) OR 10+ new LeetCode problems OR Mock SAT
        - Focus on measurable skill improvement
        - Track progress with specific metrics
        
        **IIPC (Industry Integration & Professional Connect):**
        - Monthly: LinkedIn connections (SNS15, YC startups, MNCs, academics, alumni)
        - Monthly: LinkedIn articles with hashtags #snsinstitutions #snsdesignthinkers #designthinking
        - Share experiences connecting vision/DT/5 pillars
        
        **SRI (Social Responsibility & Impact):**
        - Monthly: 1-hour DT engagement with previous schools/colleges/neighbors
        - Team activities (3-5 members)
        - Community impact focus
        
        Coaching Principles:
        1. Address identified drift issues directly
        2. Leverage student's existing strengths
        3. Create cross-pillar synergies
        4. Provide specific, measurable actions
        5. Align with career trajectory goals
        
        Generate 5-7 specific, actionable recommendations that:
        - Are tailored to the detected pattern
        - Connect multiple pillars strategically
        - Include specific platforms, timeframes, and metrics
        - Address any drift concerns identified
        
        Format each recommendation as a complete sentence with specific action items.
        """
        
        coaching_response = await self.rag_utils.generate_with_context(prompt, coaching_contexts)
        
        # Parse recommendations from response
        recommendations = []
        lines = coaching_response.split('\n')
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line[0].isdigit()):
                # Clean up formatting
                clean_line = line.lstrip('-•0123456789. ').strip()
                if clean_line:
                    recommendations.append(clean_line)
        
        return recommendations[:7]  # Limit to 7 recommendations