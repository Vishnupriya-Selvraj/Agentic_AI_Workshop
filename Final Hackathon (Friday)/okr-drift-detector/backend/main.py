import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import asyncio
from datetime import datetime
from bson import json_util

# LangGraph imports
from langgraph.prebuilt import ToolExecutor
from langgraph.graph import StateGraph, END

# Agent imports
from agents.extractor_agent import OKRExtractorAgent
from agents.trajectory_agent import TrajectoryMapperAgent
from agents.drift_agent import DriftDetectorAgent
from agents.pattern_agent import PatternClassifierAgent
from agents.coach_agent import CoachingAgent
from utils.rag_utils import GeminiRAGUtils
from models.okr_model import DriftReport, drift_reports_collection, okr_collection

# FastAPI app
app = FastAPI(title="OKR Goal-Drift Detection System")

# CORS middleware
# Update CORS middleware in main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Add your frontend port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Agent State for LangGraph
class AgentState(BaseModel):
    student_id: str
    okr_history: List[Dict[str, Any]] = []
    trajectory_summary: str = ""
    drift_report: Dict[str, Any] = {}
    pattern_classification: str = ""
    coaching_recommendations: List[str] = []
    analysis_timestamp: datetime = None

class OKRAnalysisRequest(BaseModel):
    student_id: str

class OKRDriftDetectorSystem:
    def __init__(self):
        # Initialize agents
        self.extractor_agent = OKRExtractorAgent()
        self.trajectory_agent = TrajectoryMapperAgent()
        self.drift_agent = DriftDetectorAgent()
        self.pattern_agent = PatternClassifierAgent()
        self.coach_agent = CoachingAgent()
        self.rag_utils = GeminiRAGUtils()
        
        # Create workflow
        self.create_agent_workflow()
    
    def create_agent_workflow(self):
        """Create the multi-agent workflow using LangGraph"""
        
        async def extract_okrs_node(state: AgentState) -> AgentState:
            okr_data = await self.extractor_agent.extract_past_okrs(state.student_id)
            state.okr_history = okr_data["okrs"]
            return state
        
        async def map_trajectory_node(state: AgentState) -> AgentState:
            trajectory_summary = await self.trajectory_agent.map_trajectory(
                {"okrs": state.okr_history}
            )
            state.trajectory_summary = trajectory_summary
            return state
        
        async def detect_drift_node(state: AgentState) -> AgentState:
            drift_report = await self.drift_agent.detect_drift(
                state.trajectory_summary,
                {"okrs": state.okr_history}
            )
            state.drift_report = drift_report
            return state
        
        async def classify_patterns_node(state: AgentState) -> AgentState:
            pattern_classification = await self.pattern_agent.classify_patterns(
                state.drift_report,
                state.trajectory_summary
            )
            state.pattern_classification = pattern_classification
            return state
        
        async def generate_coaching_node(state: AgentState) -> AgentState:
            coaching_recommendations = await self.coach_agent.generate_coaching(
                state.pattern_classification,
                state.drift_report,
                state.trajectory_summary
            )
            state.coaching_recommendations = coaching_recommendations
            state.analysis_timestamp = datetime.now()
            return state
        
        # Create the workflow graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("extract_okrs", extract_okrs_node)
        workflow.add_node("map_trajectory", map_trajectory_node)
        workflow.add_node("detect_drift", detect_drift_node)
        workflow.add_node("classify_patterns", classify_patterns_node)
        workflow.add_node("generate_coaching", generate_coaching_node)
        
        # Add edges
        workflow.add_edge("extract_okrs", "map_trajectory")
        workflow.add_edge("map_trajectory", "detect_drift")
        workflow.add_edge("detect_drift", "classify_patterns")
        workflow.add_edge("classify_patterns", "generate_coaching")
        workflow.add_edge("generate_coaching", END)
        
        # Set entry point
        workflow.set_entry_point("extract_okrs")
        
        # Compile the workflow
        self.app = workflow.compile()
    
    async def analyze_student(self, student_id: str) -> Dict[str, Any]:
        """Run the complete analysis for a student"""
        initial_state = AgentState(student_id=student_id)
        final_state = await self.app.ainvoke(initial_state)
        
        # Save report to MongoDB
        report = DriftReport(
            student_id=student_id,
            analysis_date=final_state.analysis_timestamp,
            trajectory_summary=final_state.trajectory_summary,
            drift_level=final_state.drift_report.get("drift_level", "Medium"),
            flagged_transitions=final_state.drift_report.get("flagged_transitions", []),
            pattern_classification=final_state.pattern_classification,
            coaching_recommendations=final_state.coaching_recommendations,
            pillar_analysis={}  # Will be populated in future versions
        )
        
        await drift_reports_collection.insert_one(report.dict())
        
        return report.dict()

# Initialize the system
system = OKRDriftDetectorSystem()

@app.post("/analyze")
async def analyze_okrs(request: OKRAnalysisRequest):
    try:
        result = await system.analyze_student(request.student_id)
        return result
    except Exception as e:
        print(f"Analysis error: {str(e)}")  # Log the error
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )
    
@app.get("/reports/{student_id}")
async def get_reports(student_id: str):
    cursor = drift_reports_collection.find(
        {"student_id": student_id}
    ).sort("analysis_date", -1).limit(5)
    
    reports = await cursor.to_list(length=None)
    return json.loads(json_util.dumps(reports))

@app.on_event("startup")
async def startup_event():
    # Initialize RAG knowledge base
    await system.rag_utils.scrape_and_store_pillar_data()

@app.get("/health")
async def health_check():
    try:
        # Verify database connection
        await okr_collection.find_one()
        return {"status": "healthy"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))