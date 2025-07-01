from typing import Dict, List, Any
from models.okr_model import okr_submissions, okr_definitions, pillars, student_collection
from utils.rag_utils import GeminiRAGUtils
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from termcolor import colored 

class OKRExtractorAgent:
    def __init__(self):
        self.rag_utils = GeminiRAGUtils()
    
    async def extract_past_okrs(self, student_id: int, cycles: int = 3) -> Dict[str, Any]:
        """Extract OKRs from the last N cycles using RAG for context"""
        print(colored(f"\n🔍 Extracting OKRs for student {student_id}", "blue"))
        
        # First verify student exists
        student = await student_collection.find_one({"_id": student_id, "isActive": True, "isDeleted": False})
        if not student:
            print(colored(f"  - Error: Student {student_id} not found or inactive", "red"))
            raise ValueError(f"Student {student_id} not found")
        
        print(colored(f"  - Student: {student['name']} ({student['registerNumber']})", "blue"))
        
        # Get distinct months from submissions
        print(colored("  - Querying distinct months...", "blue"))
        distinct_months = await okr_submissions.distinct(
            "monthId",
            {"studentId": student_id, "isActive": True, "isDeleted": False}
        )
        
        if not distinct_months:
            print(colored("  - No submissions found, using sample data", "yellow"))
            return await self._generate_sample_okrs(student_id, student)
        
        # Sort months and get last N cycles
        distinct_months.sort(reverse=True)
        last_n_months = distinct_months[:cycles]
        print(colored(f"  - Analyzing months: {', '.join(last_n_months)}", "blue"))
        
        # Query submissions for these months
        print(colored("  - Fetching submissions...", "blue"))
        cursor = okr_submissions.find({
            "studentId": student_id,
            "monthId": {"$in": last_n_months},
            "isActive": True,
            "isDeleted": False
        }).sort("monthId", -1)
        
        submissions = await cursor.to_list(length=None)
        print(colored(f"  - Found {len(submissions)} submissions", "green"))
        
        # Get related OKR definitions and pillars
        enriched_okrs = []
        print(colored("  - Enriching with OKR definitions...", "blue"))
        
        for submission in submissions:
            okr_def = await okr_definitions.find_one({"_id": submission["okrId"]})
            pillar = await pillars.find_one({"_id": submission["pillarId"]})
            
            if not okr_def or not pillar:
                print(colored(f"  - Warning: Missing definition for OKR {submission['okrId']}", "yellow"))
                continue
                
            # Use RAG to enrich OKR context
            context = self.rag_utils.query_pillar_knowledge(
                pillar["pillarName"], 
                okr_def["title"],
                k=3
            )
            
            # Format for analysis
            okr_data = {
                "monthId": submission["monthId"],
                "pillar": pillar["pillarName"],
                "title": okr_def["title"],
                "description": okr_def["description"],
                "activities": submission["activity"],
                "status": submission["status"],
                "submittedOn": submission.get("submittedOn"),
                "metadata": {
                    "okrType": okr_def["okrType"],
                    "isGroup": okr_def.get("isGroup", False),
                    "instructions": okr_def.get("instructions", [])
                },
                "context": context
            }
            enriched_okrs.append(okr_data)
        
        print(colored(f"✅ Successfully extracted {len(enriched_okrs)} enriched OKRs", "green"))
        return {
            "okrs": enriched_okrs,
            "student_info": {
                "name": student["name"],
                "register_number": student["registerNumber"],
                "department": student["department"]
            }
        }
    
async def _generate_sample_okrs(self, student_id: int, student: Dict) -> List[Dict]:
    """Generate sample OKRs based on 5-pillar framework"""
    print(colored("⚠️ Using sample OKR data", "yellow"))
    sample_okrs = [
        {
            "monthId": "2025-05",
            "pillar": "CLT",
            "title": "Value added course",
            "description": "GenAI course completion",
            "activities": [{"certificate": "https://certs.com/sample-cert"}],
            "status": "completed",
            "submittedOn": datetime.now() - timedelta(days=30),
            "metadata": {
                "okrType": "monthly",
                "isGroup": False
            }
        }
    ]
    
    return {
        "okrs": sample_okrs,
        "student_info": {
            "name": student.get("name", f"Student {student_id}"),
            "register_number": str(student.get("registerNumber", "")),  # Ensure string type
            "department": student.get("department", "")
        }
    }