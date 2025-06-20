# populate_test_data.py
from models.okr_model import okr_collection, drift_reports_collection
from datetime import datetime, timedelta

async def create_test_data():
    # Consistent student
        # Clear existing test data
    await okr_collection.delete_many({"student_id": {"$in": [
        "consistent_student",
        "exploratory_student",
        "scattered_student"
    ]}})
    
    await drift_reports_collection.delete_many({"student_id": {"$in": [
        "consistent_student",
        "exploratory_student",
        "scattered_student"
    ]}})

    await okr_collection.insert_many([
        {
            "student_id": "consistent_student",
            "cycle": "2024-Q1",
            "pillar": "CLT",
            "objective": "Learn GenAI fundamentals",
            "key_results": ["Complete course", "Build basic model"],
            "completion_status": 0.9,
            "date_created": datetime.now() - timedelta(days=90)
        },
        {
            "student_id": "consistent_student",
            "cycle": "2024-Q2",
            "pillar": "CLT",
            "objective": "Advanced GenAI applications",
            "key_results": ["Implement RAG", "Fine-tune model"],
            "completion_status": 0.7,
            "date_created": datetime.now() - timedelta(days=60)
        }
    ])
    
    # Exploratory student
    await okr_collection.insert_many([
        {
            "student_id": "exploratory_student",
            "cycle": "2024-Q1",
            "pillar": "CLT",
            "objective": "Explore GenAI",
            "key_results": ["Try different models"],
            "completion_status": 0.8,
            "date_created": datetime.now() - timedelta(days=90)
        },
        {
            "student_id": "exploratory_student",
            "cycle": "2024-Q2",
            "pillar": "CFC",
            "objective": "Try hackathon",
            "key_results": ["Join competition"],
            "completion_status": 0.6,
            "date_created": datetime.now() - timedelta(days=60)
        }
    ])
    
    # Scattered student
    await okr_collection.insert_many([
        {
            "student_id": "scattered_student",
            "cycle": "2024-Q1",
            "pillar": "CLT",
            "objective": "Learn programming",
            "key_results": ["Complete Python course"],
            "completion_status": 0.5,
            "date_created": datetime.now() - timedelta(days=90)
        },
        {
            "student_id": "scattered_student",
            "cycle": "2024-Q2",
            "pillar": "SRI",
            "objective": "Community service",
            "key_results": ["Volunteer 10 hours"],
            "completion_status": 0.3,
            "date_created": datetime.now() - timedelta(days=60)
        }
    ])

if __name__ == "__main__":
    import asyncio
    asyncio.run(create_test_data())