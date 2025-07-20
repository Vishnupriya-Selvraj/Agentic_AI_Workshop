from crewai import Task, Crew, Process
from agents import code_analyzer_agent, code_corrector_agent, manager_agent
from typing import List

# Task 1: Code Analysis
def analysis_task(agent, code: str):
    return Task(
        description="Analyze the following Python code and identify all syntax and logical errors. Return a list of errors (e.g., indentation issues, logical errors):\n" + code,
        agent=agent,
        expected_output="A list of errors found in the code.",
    )

# Task 2: Code Correction
def correction_task(agent, context, code: str):
    return Task(
        description="Fix the errors identified in the following Python code. Return the corrected code.\n" + code,
        agent=agent,
        context=[context],
        expected_output="The corrected version of the Python code.",
    )

# Crew setup and run
def run_debugging_crew(code: str):
    analyzer = code_analyzer_agent()
    corrector = code_corrector_agent()
    manager = manager_agent()

    t1 = analysis_task(analyzer, code)
    t2 = correction_task(corrector, t1, code)

    crew = Crew(
        agents=[analyzer, corrector, manager],
        tasks=[t1, t2],
        verbose=2,
        process=Process.sequential,
        planning=True
    )
    result = crew.kickoff()
    return result

if __name__ == "__main__":
    # Example input code
    code = '''
def fibonacci_iterative(n):
    if n < 0:
        return []
    elif n == 1:
        return [0]
    elif n == 2:
        return [0, 1]
    fib_sequence = [0, 1]
    for i in range(2, n):
    next_fib = fib_sequence[-1] + fib_sequence[-2]
    fib_sequence.append(next_fib)
    return fib_sequence
'''
    output = run_debugging_crew(code)
    print("\n\n### Debugging Output ###")
    print(output) 