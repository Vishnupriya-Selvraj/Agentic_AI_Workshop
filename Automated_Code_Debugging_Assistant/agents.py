import os
from crewai import Agent
from code_interpreter_tool import CodeInterpreterTool
from dotenv import load_dotenv

load_dotenv()

# Tool for code analysis
eval_tool = CodeInterpreterTool()

def code_analyzer_agent():
    return Agent(
        role="Code Analyzer",
        goal="Identify syntax and logical errors in the provided Python code.",
        backstory="Expert in Python code analysis and debugging.",
        verbose=True,
        allow_delegation=False,
        tools=[eval_tool],
    )

def code_corrector_agent():
    return Agent(
        role="Code Corrector",
        goal="Fix the identified errors in the Python code.",
        backstory="Expert in Python code correction and refactoring.",
        verbose=True,
        allow_delegation=False,
    )

def manager_agent():
    return Agent(
        role="Manager",
        goal="Oversee the code analysis and correction process, ensuring smooth task execution.",
        backstory="Experienced project manager for software debugging workflows.",
        verbose=True,
        allow_delegation=True,
    ) 