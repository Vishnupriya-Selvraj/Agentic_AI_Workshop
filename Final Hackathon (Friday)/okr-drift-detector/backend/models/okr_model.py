from datetime import datetime
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum
import motor.motor_asyncio 
from motor.motor_asyncio import AsyncIOMotorClient
import os

import pymongo

def check_db():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017")
        print("Connected to MongoDB!")
        
        # List databases
        print("Databases:", client.list_database_names())
        
        # Check okrion-v2
        db = client["okrion-v2"]
        print("Collections in okrion-v2:", db.list_collection_names())
        
        # Check student 1001
        print("Student 1001:", db.students.find_one({"_id": 1001}))
    except Exception as e:
        print("Error:", e)

check_db()

class OKRPillar(str, Enum):
    CLT = "CLT"
    CFC = "CFC"
    SCD = "SCD"
    IIPC = "IIPC"
    SRI = "SRI"
    Common = "Common"

class OKRActivity(BaseModel):
    certificate: Optional[str] = None
    leetcode: Optional[Dict[str, int]] = None
    articleUrl: Optional[str] = None
    connectedTo: Optional[str] = None
    mockTask: Optional[str] = None

class OKRSubmission(BaseModel):
    _id: int
    pillarId: int
    okrId: int
    monthId: str
    studentId: int
    activity: List[OKRActivity]
    status: str
    submittedOn: Optional[datetime] = None
    submittedBy: Optional[int] = None
    registerNumber: int
    branchId: int
    isActive: bool
    isDeleted: bool

class OKRDefinition(BaseModel):
    _id: int
    pillarId: int
    title: str
    dueDate: datetime
    description: str
    isActive: bool
    isDeleted: bool
    okrType: str
    startDate: datetime
    createdAt: datetime
    updatedAt: datetime
    __v: int
    isGroup: Optional[bool] = None
    instructions: Optional[List[str]] = None

class Pillar(BaseModel):
    _id: int
    pillarName: str
    isActive: bool
    isDeleted: bool
    createdAt: datetime
    updatedAt: datetime
    __v: int

class StudentProfile(BaseModel):
    student_id: int
    name: str
    email: str
    program: str
    year: int
    created_at: datetime = Field(default_factory=datetime.now)

class DriftReport(BaseModel):
    student_id: int
    analysis_date: datetime
    trajectory_summary: str
    drift_level: str  # Low, Medium, High
    flagged_transitions: List[Dict[str, Any]]
    pattern_classification: str
    coaching_recommendations: List[str]
    pillar_analysis: Dict[str, Any]

# MongoDB connection
client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
db = client["okrion-v2"]  # Changed to okrion_v2 database

# Collections
okr_definitions = db.okrs
pillars = db.pillars
okr_submissions = db.okrsubmissions
drift_reports = db.drift_reports
student_collection = db.students