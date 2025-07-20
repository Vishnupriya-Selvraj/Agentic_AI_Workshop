from typing import List

class ProjectSuggestionTool:
    def suggest_projects(self, topics: List[str], expertise: str) -> List[str]:
        # Simple logic for demonstration; can be replaced with LLM/tool call
        ideas = []
        for topic in topics:
            if expertise == 'beginner':
                ideas.append(f"Create a basic introduction project on {topic} (e.g., a summary or simple demo)")
            elif expertise == 'intermediate':
                ideas.append(f"Build an intermediate-level application or analysis related to {topic}")
            elif expertise == 'advanced':
                ideas.append(f"Develop an advanced, real-world project or research on {topic}")
            else:
                ideas.append(f"Project idea for {topic} (expertise level not specified)")
        return ideas 