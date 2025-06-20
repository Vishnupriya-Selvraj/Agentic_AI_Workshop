from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import motor.motor_asyncio
import os

class OKRPillar(str, Enum):
    CLT = "Continuous Learning & Training"
    CFC = "Create, Fund & Commercialize"
    SCD = "Skill & Competency Development"
    IIPC = "Industry Integration & Professional Connect"
    SRI = "Social Responsibility & Impact"

class OKRData(BaseModel):
    student_id: str
    cycle: str  # Format: "2024-Q1", "2024-M01"
    pillar: OKRPillar
    objective: str
    key_results: List[str]
    completion_status: float = Field(ge=0, le=1)
    date_created: datetime
    metadata: Dict[str, Any] = {}
    
class StudentProfile(BaseModel):
    student_id: str
    name: str
    email: str
    program: str
    year: int
    created_at: datetime = Field(default_factory=datetime.now)

class DriftReport(BaseModel):
    student_id: str
    analysis_date: datetime
    trajectory_summary: str
    drift_level: str  # Low, Medium, High
    flagged_transitions: List[Dict[str, Any]]
    pattern_classification: str
    coaching_recommendations: List[str]
    pillar_analysis: Dict[str, Any]

# MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client.okr_system

# Collections
okr_collection = db.okrs
student_collection = db.students
drift_reports_collection = db.drift_reports