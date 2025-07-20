# Financial Portfolio Manager with Autogen Agents

This project aims to build a Smart Financial Portfolio Manager that assists users in managing their investments. It leverages Microsoft Autogen's Group Chat for agent collaboration and simulates StateFlow for dynamic workflow management based on user inputs.

## Objective

To create an agentic system that analyzes a user's investment portfolio, provides tailored investment recommendations (Growth or Value), and generates a personalized financial report.

## Key Concepts Used

*   **Group Chat for Collaboration**: Agents will communicate and collaborate within a group chat managed by the `GroupChatManager` to achieve the overall goal.
*   **Dynamic Workflow Management (Simulated with StateFlow)**: The `GroupChatManager` will dynamically direct the conversation flow and agent participation based on insights from the `Portfolio_Analysis_Agent` (e.g., whether to involve the `Growth_Investment_Agent` or `Value_Investment_Agent`).
*   **Portfolio Analysis**: The `Portfolio_Analysis_Agent` summarizes the user's existing investment portfolio and determines the appropriate investment category.
*   **Investment Recommendations**: The `Growth_Investment_Agent` suggests options for maximizing portfolio growth, while the `Value_Investment_Agent` recommends stable investments for long-term value.
*   **Personalized Financial Report**: The `Investment_Advisor_Agent` compiles a detailed financial report based on all gathered insights and recommendations.

## Expected Conversation Flow

The agents interact in the following sequential pattern:

1.  **User Proxy Agent**
    *   **Role**: Initiates the chat and activates the `GroupChatManager`.
    *   **Action**: Informs the `GroupChatManager` about the user’s intention to manage their investments.

2.  **Group Chat Manager**
    *   **Role**: Manages the group chat and directs the conversation flow.
    *   **Action**: Calls the `Portfolio_Analysis_Agent` to gather user inputs.

3.  **Portfolio Analysis Agent**
    *   **Role**: Summarizes the user’s existing portfolio and determines the investment category.
    *   **Inputs Expected**: 
        *   Current salary
        *   Summary of current investment portfolio (e.g., amounts in fixed deposits, SIPs, real estate, etc.)
    *   **Output**: Explicitly states whether to pursue 'Growth' or 'Value' investments, and passes this information to the `Investment_Advisor_Agent`.

4.  **StateFlow Workflow Management (handled by GroupChatManager based on conversation)**
    *   **Role**: Dynamically directs the workflow.
    *   **Action**: Based on the `Portfolio_Analysis_Agent`'s recommendation, the `GroupChatManager` will ensure either the `Growth_Investment_Agent` or the `Value_Investment_Agent` contributes to the conversation.

5.  **Growth Investment Agent or Value Investment Agent**
    *   **Growth Investment Agent**: Suggests investments for maximizing portfolio growth.
    *   **Value Investment Agent**: Recommends stable investments for long-term value.
    *   **Action (for both)**: Provides recommendations and passes them to the `Investment_Advisor_Agent`.

6.  **Investment Advisor Agent**
    *   **Role**: Compiles a detailed report of holdings and recommendations.
    *   **Action**: Generates a personalized financial report, including portfolio analysis, investment suggestions, and a summary. Concludes with 'TERMINATE'.

## Expected Output

A personalized financial report, displayed as the final output of the `Investment_Advisor_Agent`, including portfolio analysis, growth, and value investment suggestions.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd Financial_Portfolio_Manager_Autogen
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
4.  Set up your LLM configuration. Create an `OAI_CONFIG_LIST` file (JSON format) in the `Financial_Portfolio_Manager_Autogen` directory. This file should contain a list of dictionaries, where each dictionary specifies an LLM model and its API key. For example, to use Gemini 1.5 Flash:
    ```json
    [
        {
            "model": "gemini-1.5-flash-latest",
            "api_key": "YOUR_GEMINI_API_KEY",
            "api_type": "google",
            "base_url": "https://generativelanguage.googleapis.com/v1beta/models/"
        }
    ]
    ```
    **Important**: Replace `YOUR_GEMINI_API_KEY` with your actual Google Gemini API key.

## How to Run

To run the Financial Portfolio Manager system, execute the `portfolio_manager_agents.py` script:

```bash
python portfolio_manager_agents.py
```

The `User_Proxy_Agent` will initiate the conversation. You will be prompted to provide your financial details (salary, investment portfolio summary) to guide the agent collaboration and generate your personalized financial report.

## Future Improvements

*   Integrate with real financial data APIs for live portfolio tracking.
*   Implement more sophisticated financial analysis models.
*   Allow for a wider range of investment options and user risk profiles.
*   Add a visual reporting component for charts and graphs.
*   Develop a persistent storage for user financial profiles. 