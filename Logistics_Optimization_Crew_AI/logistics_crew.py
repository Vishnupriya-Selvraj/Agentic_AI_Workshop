import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool # You might need a SerpApi key or similar for web search
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI # Import ChatGoogleGenerativeAI

load_dotenv()

# Configure Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Initialize the Gemini LLM
gemini_llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)

# Define Tools (if any, e.g., for web research)
# search_tool = SerperDevTool()

# Define the Agents
class LogisticsAgents:
    def logistics_analyst(self):
        return Agent(
            role='Logistics Analyst',
            goal='Research the current state of logistics operations, focusing on route efficiency and inventory turnover trends.',
            backstory=(
                "As a seasoned Logistics Analyst, you possess a deep understanding of supply chain dynamics."
                "You excel at gathering and interpreting data related to transportation, warehousing, and inventory."
                "Your insights are crucial for identifying bottlenecks and areas for improvement."
            ),
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm, # Assign the Gemini LLM
            # tools=[search_tool] # Uncomment if using a search tool
        )

    def optimization_strategist(self):
        return Agent(
            role='Optimization Strategist',
            goal='Create data-driven optimization strategies for logistics problems, such as delivery routes or inventory management.',
            backstory=(
                "You are an innovative Optimization Strategist with a knack for transforming data into actionable plans."
                "Your expertise lies in designing efficient and cost-effective solutions for complex logistics challenges."
                "You are adept at leveraging analytical models to propose improvements."
            ),
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm, # Assign the Gemini LLM
        )

# Define the Tasks
class LogisticsTasks:
    def research_logistics_operations(self, agent, products: list):
        return Task(
            description=f"Research the current state of logistics operations for these products: {', '.join(products)}.\n"
                        "Focus on identifying current route efficiency, common delivery issues, and inventory turnover trends."
                        "Summarize your findings with key statistics and observations.",
            agent=agent,
            expected_output="A comprehensive summary of current logistics operations, including route efficiency, delivery issues, and inventory trends for the specified products."
        )

    def develop_optimization_strategy(self, agent, context, products: list):
        return Task(
            description=f"Develop an optimization strategy for the logistics of these products: {', '.join(products)}.\n"
                        "Based on the research provided by the Logistics Analyst, propose concrete steps to improve route efficiency or inventory management.\n"
                        "Your strategy should be actionable and aim for measurable improvements.",
            agent=agent,
            context=[context],
            expected_output="A detailed optimization strategy for the logistics of the specified products, including actionable steps and potential measurable improvements."
        )

# Build the Crew
class LogisticsCrew:
    def __init__(self, products: list):
        self.products = products
        self.agents = LogisticsAgents()
        self.tasks = LogisticsTasks()

    def run(self):
        logistics_analyst_agent = self.agents.logistics_analyst()
        optimization_strategist_agent = self.agents.optimization_strategist()

        research_task = self.tasks.research_logistics_operations(logistics_analyst_agent, self.products)
        strategy_task = self.tasks.develop_optimization_strategy(optimization_strategist_agent, research_task, self.products)

        crew = Crew(
            agents=[logistics_analyst_agent, optimization_strategist_agent],
            tasks=[research_task, strategy_task],
            verbose=2, # You can set it to 1 or 2 for more detailed logs
            process=Process.sequential # Ensures tasks run in order
        )

        result = crew.kickoff()
        return result

if __name__ == "__main__":
    print("Starting Logistics Optimization Crew...")
    products_to_optimize = ["Electronics", "Perishable Goods"]
    logistics_crew = LogisticsCrew(products=products_to_optimize)
    result = logistics_crew.run()
    print("\n\n### Logistics Optimization Report ###")
    print(result) 