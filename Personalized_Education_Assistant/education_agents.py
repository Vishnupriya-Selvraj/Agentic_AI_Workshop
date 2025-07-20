import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv
from openai import OpenAI
from typing import List
from models import LearningMaterial, Quiz, ProjectIdeas, QuizQuestion
from project_suggestion_tool import ProjectSuggestionTool

load_dotenv()

SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Tool for web search
search_tool = SerperDevTool(api_key=SERPER_API_KEY)
project_tool = ProjectSuggestionTool()

# Agent 1: Learning Material Agent
def learning_material_agent():
    return Agent(
        role="Learning Material Agent",
        goal="Curate learning materials (videos, articles, exercises) for user topics.",
        backstory="Expert in educational content curation and resource discovery.",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
    )

# Agent 2: Quiz Creator Agent
def quiz_creator_agent():
    return Agent(
        role="Quiz Creator Agent",
        goal="Generate personalized quizzes for the provided topics.",
        backstory="Specialist in educational assessment and quiz generation.",
        verbose=True,
        allow_delegation=False,
    )

# Agent 3: Project Idea Agent
def project_idea_agent():
    return Agent(
        role="Project Idea Agent",
        goal="Recommend practical project ideas based on user expertise and topics.",
        backstory="Experienced in designing hands-on learning projects.",
        verbose=True,
        allow_delegation=False,
        tools=[project_tool],
    )

# Task 1: Generate learning materials
def task_learning_materials(agent, topics: List[str]):
    return Task(
        description=f"Curate a list of videos, articles, and exercises for the following topics: {', '.join(topics)}.",
        agent=agent,
        expected_output="A list of LearningMaterial objects (one per topic) with videos, articles, and exercises.",
    )

# Task 2: Create quizzes
def task_quiz(agent, context, topics: List[str]):
    return Task(
        description=f"Generate a quiz for each of the following topics: {', '.join(topics)}. Each quiz should have at least 3 questions.",
        agent=agent,
        context=[context],
        expected_output="A list of Quiz objects (one per topic) with questions, options, and answers.",
    )

# Task 3: Suggest project ideas
def task_projects(agent, context, topics: List[str], expertise: str):
    return Task(
        description=f"Suggest practical project ideas for the following topics: {', '.join(topics)}. Tailor the ideas to a user with {expertise} expertise.",
        agent=agent,
        context=[context],
        expected_output="A list of ProjectIdeas objects (one per topic) with project ideas tailored to the expertise level.",
    )

# Crew setup and run
def run_education_crew(topics: List[str], expertise: str):
    agent1 = learning_material_agent()
    agent2 = quiz_creator_agent()
    agent3 = project_idea_agent()

    t1 = task_learning_materials(agent1, topics)
    t2 = task_quiz(agent2, t1, topics)
    t3 = task_projects(agent3, t2, topics, expertise)

    crew = Crew(
        agents=[agent1, agent2, agent3],
        tasks=[t1, t2, t3],
        verbose=2,
        process=Process.sequential
    )
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    # Example usage
    topics = ["Python Programming", "Machine Learning"]
    expertise = "intermediate"
    output = run_education_crew(topics, expertise)
    print("\n\n### Personalized Education Output ###")
    print(output) 