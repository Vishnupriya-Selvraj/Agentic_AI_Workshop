# Smart Content Creation with Autogen Agents

This project simulates a two-agent conversation using Microsoft Autogen to streamline content creation and revision. A Content Creator Agent drafts content, and a Content Critic Agent evaluates it for language and technical correctness, providing constructive feedback through a reflection-based agentic pattern.

## Objective

To simulate an iterative content drafting and evaluation process using a multi-agent system, focusing on reflection and refinement based on feedback.

## Key Concepts Used

*   **Content Drafting**: The `Content_Creator` Agent drafts initial content on a specified topic (e.g., "Agentic AI").
*   **Content Evaluation**: The `Content_Critic` Agent evaluates the drafted content for clarity, conciseness, and technical accuracy.
*   **Feedback and Revision**: The `Content_Critic` provides detailed feedback, and the `Content_Creator` revises the content iteratively.
*   **Reflection-Based Agentic Pattern**: The agents engage in a conversational loop where each turn involves reflection on previous output and feedback to progressively refine the content.

## Directions and Workflow

The conversation between the two agents is designed to run for a maximum of 5 turns to simulate an iterative refinement process.

**Agent Roles:**

*   **Content Creator Agent**: Drafts content on Generative AI topics. Aims for clear, concise, and technically accurate content. Revises based on feedback and signals completion with "FINAL CONTENT:".
*   **Content Critic Agent**: Evaluates content, provides feedback on language and technical correctness, and suggests improvements. Approves satisfactory content with "Looks good! TERMINATE" or requests revisions.

**Workflow:**

1.  The `Content_Critic` Agent initiates the chat with the `Content_Creator` Agent, providing the topic.
2.  The `Content_Creator` drafts initial content.
3.  The `Content_Critic` evaluates the draft and provides feedback.
4.  The `Content_Creator` revises the content based on the feedback.
5.  This loop (feedback and revision) continues for up to 5 turns or until the `Content_Critic` approves the content.
6.  The final refined draft is extracted and displayed.

## Expected Output

The system will display the final refined content in markdown format after the conversation concludes.

## Setup and Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd Smart_Content_Creation_Autogen
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
4.  Set up your LLM configuration. Create an `OAI_CONFIG_LIST` file (JSON format) in the `Smart_Content_Creation_Autogen` directory. This file should contain a list of dictionaries, where each dictionary specifies an LLM model and its API key. For example, to use Gemini 1.5 Flash:
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
    You can include other models supported by Autogen if needed.

## How to Run

To run the Smart Content Creation system, execute the `content_agents.py` script:

```bash
python content_agents.py
```

The script will initiate the conversation between the Content Creator and Content Critic agents, and the final refined content will be displayed upon completion.

## Future Improvements

*   Allow for dynamic topic input from the user.
*   Implement more complex evaluation metrics for the Critic Agent.
*   Enable saving the conversation history and generated content to files.
*   Explore different conversational patterns beyond simple reflection. 