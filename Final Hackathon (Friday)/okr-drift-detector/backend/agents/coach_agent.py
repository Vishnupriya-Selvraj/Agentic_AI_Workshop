from utils.rag_utils import GeminiRAGUtils
from utils.tavily_client import TavilySearch
import json
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import re

class CoachingAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
        self.tavily_client = TavilySearch()
        self.pillar_okrs = {
            "CLT": ["Value Added Course"],
            "CFC": ["Hackathon", "BMC Video Analysis", "Project"],
            "SCD": ["LeetCode Problems"],
            "IIPC": ["LinkedIn Connect", "LinkedIn Article"],
            "SRI": ["DT Engagement Activity"]
        }
    
    async def _get_goal_specific_recommendations(self, goal: str, pillar: str, okr_type: str, month: int) -> List[Dict[str, str]]:
        """Get specific recommendations based on goal, pillar, OKR type and month"""
        queries = {
            "CLT": {
                "Value Added Course": {
                    1: f"beginner {goal} course 30+ hours with certification site:udemy.com OR site:coursera.org OR site:prepinsta.com",
                    2: f"intermediate {goal} course with hands-on projects site:udemy.com OR site:coursera.org",
                    3: f"advanced {goal} certification with capstone project site:udemy.com OR site:coursera.org"
                }
            },
            "CFC": {
                "Hackathon": {
                    1: f"upcoming {goal} hackathon for beginners",
                    2: f"intermediate {goal} hackathon with prizes",
                    3: f"advanced {goal} startup competition"
                },
                "BMC Video Analysis": {
                    1: f"top Y Combinator companies in {goal} field",
                    2: f"{goal} startup business model analysis",
                    3: f"{goal} unicorn company case study"
                },
                "Project": {
                    1: f"{goal} beginner project ideas",
                    2: f"intermediate {goal} project with real-world application",
                    3: f"advanced {goal} portfolio project"
                }
            },
            "SCD": {
                "LeetCode Problems": {
                    1: f"basic Python problems for {goal} applications",
                    2: f"intermediate algorithms for {goal}",
                    3: f"advanced {goal} system design problems"
                }
            },
            "IIPC": {
                "LinkedIn Connect": {
                    1: f"top {goal} professionals on LinkedIn",
                    2: f"{goal} industry mentors to connect with",
                    3: f"{goal} community leaders LinkedIn"
                },
                "LinkedIn Article": {
                    1: f"trending {goal} topics to write about",
                    2: f"{goal} project experience article examples",
                    3: f"{goal} technical article ideas"
                }
            },
            "SRI": {
                "DT Engagement Activity": {
                    1: f"simple {goal} teaching activities for beginners",
                    2: f"intermediate {goal} workshop ideas",
                    3: f"advanced {goal} mentorship program"
                }
            }
        }
        
        query = queries.get(pillar, {}).get(okr_type, {}).get(month, "")
        if not query:
            return []
            
        results = await self.tavily_client.search(query, max_results=3)
        return results

    async def _generate_project_ideas(self, goal: str, level: str) -> List[str]:
        """Generate project ideas based on goal and level"""
        prompt = f"""
        Generate 3 project ideas for a {level} level student aiming to become {goal}.
        Each idea should:
        - Be achievable in 3 months
        - Cover multiple technical aspects
        - Have clear milestones
        - Include potential real-world applications
        
        Format each idea as:
        1. [Project Name]
           - Objective: 
           - Key Technologies: 
           - Monthly Milestones:
             - Month 1: 
             - Month 2: 
             - Month 3: 
           - Potential Impact:
        """
        
        response = await self.rag_utils.generate_with_context(prompt)
        return response.split('\n')

    async def generate_coaching(self, pattern: str, drift_report: Dict[str, Any], 
                          trajectory: str, quarterly_goal: str = None,
                          current_level: str = "beginner") -> Dict[str, Any]:
        """Generate coaching with proper parameter defaults"""
        if not quarterly_goal:
            quarterly_goal = "career development"
            print("⚠️ No quarterly goal provided, using default")
        quarterly_plan = {}
        
        for month in range(1, 4):
            monthly_plan = {}
            for pillar, okr_types in self.pillar_okrs.items():
                pillar_plan = {}
                for okr_type in okr_types:
                    if okr_type == "Project" and month == 1:
                        # Only generate project ideas in month 1
                        if pillar == "CFC":
                            project_ideas = await self._generate_project_ideas(quarterly_goal, current_level)
                            pillar_plan[okr_type] = {
                                "ideas": project_ideas,
                                "action": self._get_okr_action(pillar, okr_type, month)
                            }
                    else:
                        recommendations = await self._get_goal_specific_recommendations(
                            quarterly_goal, pillar, okr_type, month
                        )
                        if recommendations:
                            pillar_plan[okr_type] = {
                                "recommendations": [
                                    {
                                        "title": rec.get("title", ""),
                                        "url": rec.get("url", ""),
                                        "description": rec.get("content", "")[:200] + "..."
                                    }
                                    for rec in recommendations
                                ],
                                "action": self._get_okr_action(pillar, okr_type, month),
                                "success_metrics": self._get_success_metrics(pillar, okr_type, month)
                            }
                monthly_plan[pillar] = pillar_plan
            quarterly_plan[f"Month {month}"] = monthly_plan
        
        return {
            "quarterly_roadmap": quarterly_plan,
            "goal_alignment": self._generate_goal_alignment_analysis(quarterly_goal, current_level),
            "cross_pillar_synergies": self._generate_cross_pillar_synergies(quarterly_goal)
        }

    def _get_okr_action(self, pillar: str, okr_type: str, month: int) -> str:
        """Get specific action items for each OKR type"""
        actions = {
            "CLT": {
                "Value Added Course": {
                    1: "Complete beginner course with certification (30+ hours)",
                    2: "Finish intermediate course with project submission",
                    3: "Complete advanced certification and build portfolio project"
                }
            },
            "CFC": {
                "Hackathon": {
                    1: "Participate in beginner hackathon and submit project",
                    2: "Join intermediate competition and reach semifinals",
                    3: "Compete in advanced challenge and get feedback from judges"
                },
                "BMC Video Analysis": {
                    1: "Analyze 3 YC companies in your field",
                    2: "Compare business models of 2 successful startups",
                    3: "Create your own BMC for your project"
                },
                "Project": {
                    1: "Define project scope and setup development environment",
                    2: "Complete core functionality and initial testing",
                    3: "Finalize project and prepare documentation"
                }
            },
            "SCD": {
                "LeetCode Problems": {
                    1: "Solve 20 beginner problems with 90% accuracy",
                    2: "Complete 15 intermediate challenges",
                    3: "Master 10 advanced algorithms with optimal solutions"
                }
            },
            "IIPC": {
                "LinkedIn Connect": {
                    1: "Connect with 5 professionals and initiate conversations",
                    2: "Get 2 informational interviews with experts",
                    3: "Secure 1 mentorship connection"
                },
                "LinkedIn Article": {
                    1: "Publish 1 article about beginner learnings",
                    2: "Write about project development experience",
                    3: "Create technical article showcasing expertise"
                }
            },
            "SRI": {
                "DT Engagement Activity": {
                    1: "Teach 5 people basic concepts",
                    2: "Conduct workshop for 10+ participants",
                    3: "Mentor 2 beginners through their first project"
                }
            }
        }
        return actions.get(pillar, {}).get(okr_type, {}).get(month, "")

    def _get_success_metrics(self, pillar: str, okr_type: str, month: int) -> List[str]:
        """Get measurable success metrics for each OKR"""
        metrics = {
            "CLT": {
                "Value Added Course": [
                    "Course completion certificate",
                    "Project submission (if applicable)",
                    "Self-assessment quiz score >85%"
                ]
            },
            "CFC": {
                "Hackathon": [
                    "Participation certificate",
                    "Project submission",
                    "Judge feedback (if available)"
                ],
                "BMC Video Analysis": [
                    "Completed BMC worksheets",
                    "Key insights documented",
                    "Comparison analysis report"
                ],
                "Project": [
                    "GitHub repository with code",
                    "Documentation",
                    "Demo video or live demo"
                ]
            },
            "SCD": {
                "LeetCode Problems": [
                    "Number of problems solved",
                    "Accuracy rate",
                    "Time complexity improvements"
                ]
            },
            "IIPC": {
                "LinkedIn Connect": [
                    "Number of new connections",
                    "Response rate",
                    "Informational interviews secured"
                ],
                "LinkedIn Article": [
                    "Article published",
                    "Engagement metrics (likes, comments)",
                    "Profile view increase"
                ]
            },
            "SRI": {
                "DT Engagement Activity": [
                    "Number of participants",
                    "Feedback scores",
                    "Documented impact"
                ]
            }
        }
        return metrics.get(pillar, {}).get(okr_type, [])

    def _generate_goal_alignment_analysis(self, goal: str, level: str) -> str:
        """Generate analysis of how recommendations align with goal"""
        return f"""
        The recommendations are specifically tailored for a {level} level student aiming to become {goal}.
        - Course progression follows beginner → intermediate → advanced track
        - Hackathons and projects focus on {goal} applications
        - Coding problems selected for {goal} relevance
        - Networking targets {goal} professionals
        - Teaching activities build {goal} communication skills
        """

    def _generate_cross_pillar_synergies(self, goal: str) -> List[str]:
        """Identify connections between pillars"""
        return [
            f"CLT courses provide knowledge for CFC projects and IIPC articles about {goal}",
            f"SCD coding skills improve CFC project quality in {goal}",
            f"IIPC connections can lead to SRI mentorship opportunities in {goal}",
            f"CFC projects can be showcased in IIPC articles about {goal}",
            f"SRI teaching reinforces CLT learning about {goal}"
        ]