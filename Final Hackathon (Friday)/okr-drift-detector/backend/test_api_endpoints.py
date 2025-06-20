import httpx
import asyncio
from datetime import datetime

BASE_URL = "http://localhost:8000"

async def test_health_check():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        assert response.status_code == 200
        print("Health Check:", response.json())

async def test_analysis_workflow(student_id):
    async with httpx.AsyncClient() as client:
        # Run analysis
        response = await client.post(
            f"{BASE_URL}/analyze",
            json={"student_id": student_id}
        )
        
        if response.status_code != 200:
            print(f"Analysis failed for {student_id}: {response.text}")
            return None
        
        result = response.json()
        print(f"\nAnalysis Result for {student_id}:")
        print(f"Pattern: {result.get('pattern_classification', 'N/A')}")
        print(f"Drift Level: {result.get('drift_level', 'N/A')}")
        print("Recommendations:")
        for i, rec in enumerate(result.get('coaching_recommendations', [])[:3], 1):
            print(f" {i}. {rec}")
        
        return result

async def test_report_retrieval(student_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/reports/{student_id}")
        if response.status_code != 200:
            print(f"Failed to get reports: {response.text}")
            return []
        
        reports = response.json()
        print(f"\nFound {len(reports)} reports for {student_id}")
        if reports:
            print(f"Latest report created at: {reports[0].get('analysis_date')}")
        return reports

async def main():
    print("Starting API Tests")
    
    await test_health_check()
    
    test_students = [
        "consistent_student",
        "exploratory_student",
        "scattered_student"
    ]
    
    for student_id in test_students:
        await test_analysis_workflow(student_id)
        await test_report_retrieval(student_id)
    
    print("\n=== Testing Completed ===")

if __name__ == "__main__":
    asyncio.run(main())