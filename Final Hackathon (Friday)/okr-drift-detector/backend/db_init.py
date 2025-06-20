# db_init.py
import asyncio
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
from okr_model import OKRData, DriftReport

async def init_db():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    db = client.okr_system
    
    # Sample OKRs
    sample_okrs = [
        {
            "student_id": "student_123",
            "cycle": "2024-Q1",
            "pillar": "CLT",
            "objective": "Complete GenAI course and build first AI project",
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
            "student_id": "student_123",
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
        }
    ]
    
    await db.okrs.insert_many(sample_okrs)
    
    # Sample drift report
    report = DriftReport(
        student_id="student_123",
        analysis_date=datetime.now(),
        trajectory_summary="Progressive focus on AI specialization",
        drift_level="Medium",
        flagged_transitions=[{
            "from": "GenAI Course Completion (CLT)",
            "to": "Competitive Programming Focus (SCD)",
            "reason": "Sudden shift from AI learning to algorithmic problem solving"
        }],
        pattern_classification="Iterative Refinement with some exploration",
        coaching_recommendations=[
            "Connect GenAI skills with hackathon projects",
            "Focus on AI/ML algorithm problems in LeetCode"
        ],
        pillar_analysis={}
    )
    
    await db.drift_reports.insert_one(report.dict())

if __name__ == "__main__":
    asyncio.run(init_db())