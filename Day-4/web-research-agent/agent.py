import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient

# Load API keys from .env
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Initialize clients
groq_client = Groq(api_key=GROQ_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

class ResearchAgent:
    def __init__(self, topic):
        self.topic = topic
        self.questions = []
        self.answers = {}

    # Step 1: Reasoning (Planning phase)
    def generate_questions(self):
        prompt = f"""Generate 5 to 6 deep and varied research questions about the topic: "{self.topic}".
Include aspects such as causes, impacts, history, future trends, technologies, and policies."""

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content
        self.questions = [q.strip("-•1234567890. ").strip() for q in content.split("\n") if q.strip()]
        return self.questions

    # Step 2: Acting (searching the web)
    def search_answers(self):
        for question in self.questions:
            result = tavily_client.search(query=question, include_raw_content=True)
            self.answers[question] = []
            for item in result["results"][:3]:  # Top 3 results
                title = item["title"]
                content = item["content"][:300]  # Trim for clarity
                self.answers[question].append(f"**{title}**\n{content}...\n")
        return self.answers

    # Step 3: Report generation
    def compile_report(self):
        report = f"# Web Research Report on: {self.topic}\n\n"
        report += "## Introduction\nThis report explores major questions about the given topic using real-time web data and LLM reasoning.\n\n"
        
        for question in self.questions:
            report += f"## {question}\n"
            for answer in self.answers.get(question, []):
                report += answer + "\n"
        
        report += "\n## Conclusion\nThis structured research summarizes the key insights collected from the web on the topic.\n"
        return report
