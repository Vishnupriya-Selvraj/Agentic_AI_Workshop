# Bill Managing Agent with Autogen

This project develops a Bill Management Agent using Microsoft Autogen's Group Chat for agent collaboration. The system is designed to help users efficiently track and understand their expenses by processing bill images, categorizing expenditures, calculating totals, and providing insights into spending patterns.

## Objective

To create a multi-agent system that automates the process of expense tracking and analysis from bill images, providing users with a clear overview of their spending.

## Key Concepts Used

*   **Group Agent Conversation**: Agents interact collaboratively within a group chat environment managed by the `GroupChatManager`.
*   **Chat Initiation**: The `User_Proxy_Agent` initiates the conversation, acting as the interface between the user and the agent system.
*   **Bill Processing (Simulated)**: The `Bill_Processing_Agent` is responsible for extracting data from bill images and organizing expenses into predefined categories (e.g., groceries, dining, utilities, shopping, entertainment). For this project, image processing is simulated using a dummy function.
*   **Expense Summarization**: The `Expense_Summarization_Agent` analyzes the extracted and categorized expenses to provide a breakdown of total spending per category and highlight spending trends.

## Workflow

The agents interact in the following sequential pattern:

1.  **User Proxy Agent**
    *   **Role**: Initiates a conversation with the `GroupChatManager`.
    *   **Action**: Provides the path to a bill image that needs to be processed.

2.  **Bill Processing Agent**
    *   **Role**: Extracts and categorizes expenses from the input bill image.
    *   **Expected Input**: Image path of a bill or receipt.
    *   **Expected Output**: A categorized list of all expenses with the total amount spent.

3.  **Expense Summarization Agent**
    *   **Role**: Analyzes the extracted expenses and provides a breakdown of total spending per category.
    *   **Expected Input**: Categorized list of expenses from the `Bill_Processing_Agent`.
    *   **Expected Output**: A summary of spending trends, highlighting categories with the highest expenditure.

## Expected Final Output

The Bill Management Agent will provide an insightful and actionable summary of spending trends, ensuring a sequential conversational experience.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd Bill_Managing_Agent_Autogen
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
4.  Set up your LLM configuration. Create an `OAI_CONFIG_LIST` file (JSON format) in the `Bill_Managing_Agent_Autogen` directory. This file should contain a list of dictionaries, where each dictionary specifies an LLM model and its API key. For example, to use Gemini 1.5 Flash:
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

To run the Bill Managing Agent system, execute the `bill_agents.py` script:

```bash
python bill_agents.py
```

The script will create a dummy image file (`dummy_bill.png`) and then initiate the conversation with the `User_Proxy_Agent`, who will provide the path to this dummy image. The agents will then collaborate to process and summarize the expenses.

## Future Improvements

*   Integrate with actual OCR (Optical Character Recognition) services to process real bill images.
*   Implement more sophisticated expense categorization using machine learning.
*   Develop a user interface for uploading bills and viewing spending insights.
*   Allow for multi-currency support and currency conversion.
*   Add persistent storage for expense history and spending patterns. 