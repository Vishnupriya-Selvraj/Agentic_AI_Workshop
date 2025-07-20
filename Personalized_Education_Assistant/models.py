from pydantic import BaseModel
from typing import List

class LearningMaterial(BaseModel):
    topic: str
    videos: List[str]
    articles: List[str]
    exercises: List[str]

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    answer: str

class Quiz(BaseModel):
    topic: str
    questions: List[QuizQuestion]

class ProjectIdeas(BaseModel):
    topic: str
    expertise: str
    ideas: List[str] 