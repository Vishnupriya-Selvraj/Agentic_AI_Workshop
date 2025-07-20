# Logistics Optimization Analysis with Crew AI

This project implements a Crew AI system to analyze logistics data and develop optimization strategies. It focuses on solving specific logistics industry problems, such as optimizing delivery routes or inventory management, through collaborative agent-based analysis.

## Objective

To create a Crew AI system capable of researching current logistics operations and developing data-driven optimization strategies.

## Instructions and Workflow

This system involves two specialized agents collaborating to achieve logistics optimization:

### 1. Define Roles:

*   **Logistics Analyst**:
    *   **Goal**: Research the current state of logistics operations, focusing on route efficiency and inventory turnover trends.
    *   **Backstory**: "As a seasoned Logistics Analyst, you possess a deep understanding of supply chain dynamics. You excel at gathering and interpreting data related to transportation, warehousing, and inventory. Your insights are crucial for identifying bottlenecks and areas for improvement."

*   **Optimization Strategist**:
    *   **Goal**: Create data-driven optimization strategies for logistics problems, such as delivery routes or inventory management.
    *   **Backstory**: "You are an innovative Optimization Strategist with a knack for transforming data into actionable plans. Your expertise lies in designing efficient and cost-effective solutions for complex logistics challenges. You are adept at leveraging analytical models to propose improvements."

### 2. Define Tasks:

*   **Research Logistics Operations (assigned to Logistics Analyst)**:
    *   **Description**: Research the current state of logistics operations for a given list of products. Focus on identifying current route efficiency, common delivery issues, and inventory turnover trends. Summarize findings with key statistics and observations.
    *   **Parametrization**: The task is parameterized to accept a list of products (e.g., `["Electronics", "Perishable Goods"]`).

*   **Develop Optimization Strategy (assigned to Optimization Strategist)**:
    *   **Description**: Develop an optimization strategy for the logistics of the specified products. Based on the research provided by the Logistics Analyst, propose concrete steps to improve route efficiency or inventory management. The strategy should be actionable and aim for measurable improvements.
    *   **Parametrization**: The task is parameterized to accept a list of products and the context (output from the research task).

### 3. Build the Crew:

The Crew is set up with the two agents and their tasks, ensuring a sequential process (`Process.sequential`) where the Logistics Analyst completes its research before the Optimization Strategist develops a strategy.

## Expected Output

The system will produce a comprehensive logistics optimization report, detailing the current state of operations and a proposed optimization strategy for the specified products.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd Logistics_Optimization_Crew_AI
    ```
2.  Create a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: `venv\Scripts\activate`
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up your LLM Configuration and API Keys**:
    *   Crew AI can utilize various LLMs. It often defaults to OpenAI models if `OPENAI_API_KEY` is set in your environment variables.
    *   **For Gemini**: Create a `.env` file in the `Logistics_Optimization_Crew_AI` directory and set your Gemini API key as `GOOGLE_API_KEY`. You may also need to explicitly tell Crew AI to use the Google model. In `logistics_crew.py`, the line `os.environ["OPENAI_API_KEY"] = os.getenv("GEMINI_API_KEY")` attempts to map the Gemini key to what Crew AI might expect for a generic OpenAI-compatible setup, but direct Google model integration might require `crewai[google]` installation and explicit model configuration within the `Agent` definition.
    *   **Important**: Ensure you have a valid API key set for the LLM you intend to use.

## How to Run

To run the Logistics Optimization Crew AI system, execute the `logistics_crew.py` script:

```bash
python logistics_crew.py
```

The script will initiate the Crew AI workflow with predefined products (`["Electronics", "Perishable Goods"]`). The agents will collaborate to research logistics operations and develop an optimization strategy, and the final report will be displayed.

## Future Improvements

*   Integrate with real logistics data (e.g., shipment tracking, inventory databases).
*   Implement more sophisticated optimization algorithms for route planning and inventory control.
*   Allow for dynamic product lists and industry-specific problem definitions from user input.
*   Add a visualization component for routes and inventory trends.
*   Develop a feedback loop for strategists to refine their recommendations based on implementation results. 