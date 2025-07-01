# main.py
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional, TypedDict
from datetime import datetime
from bson import json_util
import sys
import time
import asyncio
from termcolor import colored
from enum import Enum
from utils.tavily_client import TavilySearch

# LangGraph imports
from langgraph.graph import StateGraph, END
from langchain_core.runnables import RunnableLambda

# Agent imports
from agents.extractor_agent import OKRExtractorAgent
from agents.trajectory_agent import TrajectoryMapperAgent
from agents.drift_agent import DriftDetectorAgent
from agents.pattern_agent import PatternClassifierAgent
from agents.coach_agent import CoachingAgent
from utils.rag_utils import GeminiRAGUtils
from models.okr_model import db, drift_reports, student_collection, okr_submissions

app = FastAPI(title="OKR Goal-Drift Detection System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentState(TypedDict):
    student_id: int
    student_name: str
    register_number: str
    quarterly_goal: str  # Add this line
    current_level: str  # Add this line
    okr_history: List[Dict[str, Any]]
    trajectory_summary: str
    drift_report: Dict[str, Any]
    pattern_classification: str
    coaching_recommendations: List[str]
    analysis_timestamp: datetime
    messages: List[Dict[str, Any]]
    progress: Optional[Any]

class NodeType(str, Enum):
    EXTRACT_OKRS = "extract_okrs"
    MAP_TRAJECTORY = "map_trajectory"
    DETECT_DRIFT = "detect_drift"
    CLASSIFY_PATTERNS = "classify_patterns"
    GENERATE_COACHING = "generate_coaching"

class TerminalProgress:
    def __init__(self, total_steps=5):
        self.total_steps = total_steps
        self.current_step = 0
        self.start_time = time.time()
    
    def start(self, student_name: str):
        print(colored(f"\n🚀 Starting OKR Goal-Drift Analysis for {student_name}", "cyan", attrs=["bold"]))
        print(colored("="*60, "cyan"))
    
    def update(self, message, status="info"):
        self.current_step += 1
        elapsed = time.time() - self.start_time
        color = {
            "info": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red"
        }.get(status, "white")
        
        print(colored(
            f"\n🔹 Step {self.current_step}/{self.total_steps}: {message} "
            f"(Elapsed: {elapsed:.2f}s)",
            color
        ))
        sys.stdout.flush()
    
    def complete(self):
        total_time = time.time() - self.start_time
        print(colored("\n✅ Analysis Complete!", "green", attrs=["bold"]))
        print(colored(f"⏱️  Total Time: {total_time:.2f} seconds", "green"))
        print(colored("="*60 + "\n", "cyan"))

class OKRAnalysisRequest(BaseModel):
    student_id: int
    quarterly_goal: str = Field(default="career development", description="Student's goal for the quarter")
    current_level: str = Field(default="beginner", description="Current skill level")

    
class OKRDriftDetectorSystem:
    def __init__(self):
        self.extractor_agent = OKRExtractorAgent()
        self.trajectory_agent = TrajectoryMapperAgent()
        self.drift_agent = DriftDetectorAgent()
        self.pattern_agent = PatternClassifierAgent()
        self.coach_agent = CoachingAgent()
        self.rag_utils = GeminiRAGUtils()
        self.tavily_client = TavilySearch()

        # Define tools
        self.tools = {
            "extract_okrs": RunnableLambda(self._extract_okrs_tool),
            "map_trajectory": RunnableLambda(self._map_trajectory_tool),
            "detect_drift": RunnableLambda(self._detect_drift_tool),
            "classify_patterns": RunnableLambda(self._classify_patterns_tool),
            "generate_coaching": RunnableLambda(self._generate_coaching_tool)
        }
        
        self.workflow = self._create_workflow()

    async def _extract_okrs_tool(self, student_id: int) -> Dict[str, Any]:
        """Tool to extract OKRs from database"""
        okr_data = await self.extractor_agent.extract_past_okrs(student_id)
        return {
            "okr_history": okr_data["okrs"],
            "student_name": okr_data["student_info"]["name"],
            "register_number": okr_data["student_info"]["register_number"]
        }

    async def _map_trajectory_tool(self, okr_history: List[Dict[str, Any]]) -> str:
        """Tool to map learning trajectory"""
        trajectory_summary = await self.trajectory_agent.map_trajectory({"okrs": okr_history})
        return trajectory_summary

    async def _detect_drift_tool(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Tool to detect goal drift"""
        drift_report = await self.drift_agent.detect_drift(
            state["trajectory_summary"],
            {"okrs": state["okr_history"]}
        )
        return drift_report

    async def _classify_patterns_tool(self, state: Dict[str, Any]) -> str:
        """Tool to classify behavioral patterns"""
        pattern_classification = await self.pattern_agent.classify_patterns(
            state["drift_report"],
            state["trajectory_summary"]
        )
        return pattern_classification

    async def _generate_coaching_tool(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Tool to generate coaching recommendations"""
        coaching_recommendations = await self.coach_agent.generate_coaching(
            state["pattern_classification"],
            state["drift_report"],
            state["trajectory_summary"],
            state["quarterly_goal"],
            state["current_level"]
        )
        return coaching_recommendations

    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        
        def should_continue(state: AgentState) -> str:
            if "okr_history" not in state or not state["okr_history"]:
                return NodeType.EXTRACT_OKRS
            elif "trajectory_summary" not in state:
                return NodeType.MAP_TRAJECTORY
            elif "drift_report" not in state:
                return NodeType.DETECT_DRIFT
            elif "pattern_classification" not in state:
                return NodeType.CLASSIFY_PATTERNS
            elif "coaching_recommendations" not in state:
                return NodeType.GENERATE_COACHING
            else:
                return END

        async def extract_okrs_node(state: AgentState) -> Dict[str, Any]:
            if state.get("progress"):
                state["progress"].update("Extracting student OKR history from database")
            
            result = await self._extract_okrs_tool(state["student_id"])
            return {
                **state,
                "okr_history": result["okr_history"],
                "student_name": result["student_name"],
                "register_number": result["register_number"]
            }

        async def map_trajectory_node(state: AgentState) -> Dict[str, Any]:
            if state.get("progress"):
                state["progress"].update("Mapping learning trajectory across OKR cycles")
            
            trajectory_summary = await self.trajectory_agent.map_trajectory(
                {"okrs": state["okr_history"]},
                state["quarterly_goal"]  # Pass the goal
            )
            return {
                **state,
                "trajectory_summary": trajectory_summary
            }

        async def detect_drift_node(state: AgentState) -> Dict[str, Any]:
            if state.get("progress"):
                state["progress"].update("Analyzing goal drift patterns")
            
            drift_report = await self.drift_agent.detect_drift(
                state["trajectory_summary"],
                {"okrs": state["okr_history"]},
                state["quarterly_goal"]  # Pass the goal
            )
            return {
                **state,
                "drift_report": drift_report
            }

        async def classify_patterns_node(state: AgentState) -> Dict[str, Any]:
            if state.get("progress"):
                state["progress"].update("Classifying behavioral patterns")
            
            pattern_classification = await self.pattern_agent.classify_patterns(
                state["drift_report"],
                state["trajectory_summary"],
                state["quarterly_goal"]  # Pass the goal
            )
            return {
                **state,
                "pattern_classification": pattern_classification
            }

        async def generate_coaching_node(state: AgentState) -> Dict[str, Any]:
            if state.get("progress"):
                state["progress"].update("Generating coaching recommendations")
            
            coaching_recommendations = await self._generate_coaching_tool(state)
            return {
                **state,
                "coaching_recommendations": coaching_recommendations,
                "analysis_timestamp": datetime.now()
            }

        workflow = StateGraph(AgentState)
        
        workflow.add_node(NodeType.EXTRACT_OKRS, extract_okrs_node)
        workflow.add_node(NodeType.MAP_TRAJECTORY, map_trajectory_node)
        workflow.add_node(NodeType.DETECT_DRIFT, detect_drift_node)
        workflow.add_node(NodeType.CLASSIFY_PATTERNS, classify_patterns_node)
        workflow.add_node(NodeType.GENERATE_COACHING, generate_coaching_node)
        
        workflow.add_edge(NodeType.EXTRACT_OKRS, NodeType.MAP_TRAJECTORY)
        workflow.add_edge(NodeType.MAP_TRAJECTORY, NodeType.DETECT_DRIFT)
        workflow.add_edge(NodeType.DETECT_DRIFT, NodeType.CLASSIFY_PATTERNS)
        workflow.add_edge(NodeType.CLASSIFY_PATTERNS, NodeType.GENERATE_COACHING)
        workflow.add_edge(NodeType.GENERATE_COACHING, END)
        
        workflow.set_entry_point(NodeType.EXTRACT_OKRS)
        
        return workflow.compile()

    def _generate_pillar_analysis(self, okr_history: List[Dict]) -> Dict[str, Any]:
        """Generate pillar analysis scores based on OKR history"""
        pillar_scores = {
            "CLT": {"score": 0, "focus": "", "completion": 0, "trend": "stable"},
            "CFC": {"score": 0, "focus": "", "completion": 0, "trend": "stable"},
            "SCD": {"score": 0, "focus": "", "completion": 0, "trend": "stable"},
            "IIPC": {"score": 0, "focus": "", "completion": 0, "trend": "stable"},
            "SRI": {"score": 0, "focus": "", "completion": 0, "trend": "stable"}
        }
        
        # Count OKRs per pillar and track focus areas
        pillar_counts = {p: 0 for p in pillar_scores.keys()}
        pillar_focus = {p: {} for p in pillar_scores.keys()}  # Track frequency of focus areas
        
        for okr in okr_history:
            pillar = okr.get("pillar")
            if pillar in pillar_counts:
                pillar_counts[pillar] += 1
                
                # Extract focus from title or description
                focus_text = okr.get("title", "").lower() + " " + okr.get("description", "").lower()
                
                # Common focus areas for each pillar
                focus_keywords = {
                    "CLT": ["genai", "course", "learning", "product management", "innovation"],
                    "CFC": ["hackathon", "project", "startup", "business model", "commercial"],
                    "SCD": ["leetcode", "competitive", "exam", "skill", "programming"],
                    "IIPC": ["linkedin", "network", "article", "professional", "connect"],
                    "SRI": ["community", "design thinking", "social", "responsibility", "impact"]
                }
                
                # Find most relevant focus keyword
                for keyword in focus_keywords.get(pillar, []):
                    if keyword in focus_text:
                        pillar_focus[pillar][keyword] = pillar_focus[pillar].get(keyword, 0) + 1
        
        # Calculate scores and determine focus
        total_okrs = len(okr_history)
        for pillar, count in pillar_counts.items():
            if total_okrs > 0:
                score = min(100, int((count / total_okrs) * 100 * 2))  # Scale to make scores meaningful
                pillar_scores[pillar]["score"] = score
                pillar_scores[pillar]["completion"] = score
                
                # Determine focus area
                if pillar_focus[pillar]:
                    most_common_focus = max(pillar_focus[pillar].items(), key=lambda x: x[1])[0]
                    pillar_scores[pillar]["focus"] = most_common_focus.title()
                else:
                    pillar_scores[pillar]["focus"] = "General"  # Default if no specific focus
                
                # Simple trend calculation
                if score > 60:
                    pillar_scores[pillar]["trend"] = "up"
                elif score < 40:
                    pillar_scores[pillar]["trend"] = "down"
        
        return pillar_scores

    async def analyze_student(self, student_id: int, quarterly_goal: str, current_level: str) -> Dict[str, Any]:
        """Run the complete analysis for a student"""
        progress = TerminalProgress(total_steps=5)
    
        student = await student_collection.find_one({"_id": student_id})
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
        
        progress.start(student["name"])
        
        initial_state = AgentState(
            student_id=student_id,
            student_name=student["name"],
            register_number=student["registerNumber"],
            quarterly_goal=quarterly_goal,  # Explicitly set here
            current_level=current_level,
            okr_history=[],
            trajectory_summary="",
            drift_report={},
            pattern_classification="",
            coaching_recommendations=[],
            analysis_timestamp=datetime.now(),
            messages=[],
            progress=progress
        )
        
        workflow_result = await self.workflow.ainvoke(initial_state)
        
        report = {
            "student_info": {
                "id": workflow_result["student_id"],
                "name": workflow_result["student_name"],
                "register_number": workflow_result["register_number"]
            },
            "goal_analysis": {
                "quarterly_goal": quarterly_goal,
                "current_level": current_level,
                "readiness_score": self._calculate_readiness_score(workflow_result["okr_history"])
            },
            "drift_analysis": workflow_result["drift_report"],
            "pattern_analysis": workflow_result["pattern_classification"],
            "coaching_plan": workflow_result["coaching_recommendations"],
            "pillar_analysis": self._generate_pillar_analysis(workflow_result["okr_history"]),
            "analysis_date": workflow_result["analysis_timestamp"]
        }
        
        await drift_reports.insert_one(report)
        progress.complete()
        
        return report

    def _calculate_readiness_score(self, okr_history: List[Dict]) -> int:
        """Calculate how prepared the student is for their goal"""
        relevant_okrs = [okr for okr in okr_history 
                        if okr.get("pillar") in ["CLT", "CFC", "SCD"]]
        return min(100, len(relevant_okrs) * 10)  # Simple metric - improve as needed

system = OKRDriftDetectorSystem()

@app.post("/analyze")
async def analyze_okrs(request: OKRAnalysisRequest):
    try:
        print(colored(f"\n🔎 Received analysis request for student ID: {request.student_id}", "blue"))
        print(colored(f"🎯 Quarterly Goal: {request.quarterly_goal}", "cyan"))
        print(colored(f"📊 Current Level: {request.current_level}", "cyan"))
        
        result = await system.analyze_student(
            request.student_id, 
            request.quarterly_goal,
            request.current_level
        )
        
        return json.loads(json_util.dumps(result))
    except Exception as e:
        print(colored(f"\n❌ Analysis error: {str(e)}", "red"))
        raise HTTPException(status_code=500, detail=str(e))
        
@app.get("/reports/{student_id}")
async def get_reports(student_id: int):
    print(colored(f"\n📂 Fetching reports for student ID: {student_id}", "blue"))
    cursor = drift_reports.find(
        {"student_id": student_id}
    ).sort("analysis_date", -1).limit(5)
    
    reports = await cursor.to_list(length=None)
    return json.loads(json_util.dumps(reports))

@app.on_event("startup")
async def startup_event():
    print(colored("\n🔌 Initializing OKR Goal-Drift Detection System...", "cyan"))
    
    # Initialize with retry logic
    max_retries = 3
    for attempt in range(max_retries):
        try:
            print(colored(f"📚 Loading RAG knowledge base (attempt {attempt+1})...", "blue"))
            await system.rag_utils.fetch_and_store_pillar_data()
            break
        except Exception as e:
            print(colored(f"⚠️ Startup error: {str(e)}", "yellow"))
            if attempt == max_retries - 1:
                print(colored("❌ Failed to initialize after multiple attempts", "red"))
                raise
            await asyncio.sleep(2)
    
    print(colored("✅ System ready to accept requests", "green"))

@app.get("/health")
async def health_check():
    try:
        # Verify database connection
        await okr_submissions.find_one()
        return {"status": "healthy"}
    except Exception as e:
        print(colored(f"\n❌ Health check failed: {str(e)}", "red"))
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/db-status")
async def check_db_status():
    try:
        # Test connection and collection access
        collections = await db.list_collection_names()
        student_count = await db.students.count_documents({})
        
        return {
            "database": db.name,
            "collections": collections,
            "student_count": student_count,
            "status": "connected"
        }
    except Exception as e:
        return {"status": "error", "details": str(e)}