# LangGraph Math Agent

This project implements an AI agent using LangGraph that can answer general questions using a Large Language Model (LLM) and perform mathematical operations (addition, subtraction, multiplication, and division) by calling predefined functions.

## Problem Statement

Create an agent using LangGraph that answers general questions using the LLM, and when asked to perform mathematical operations (addition, subtraction, multiplication, and division), it calls four predefined functions (plus, divide, sub, mul) for answering. The agent should handle both general and math-related queries seamlessly.

## Requirements

1.  **LLM Integration**: Uses the Groq API (or a similar LLM API) for general reasoning.
2.  **Custom Mathematical Functions**: Four Python functions (`plus`, `subtract`, `multiply`, `divide`) are defined to handle arithmetic operations.
3.  **Conditional Routing**: The agent detects mathematical queries and routes them to the appropriate custom function; otherwise, it forwards the query to the LLM for a general response.
4.  **LangGraph for Flow Control**: The entire logic, including tool integration and conditional transitions, is orchestrated using LangGraph.

## Architecture and Flow

The agent's workflow is managed by a LangGraph `StateGraph` with the following key components:

*   **AgentState**: A `TypedDict` that maintains the conversation history as a list of `BaseMessage` objects.
*   **Nodes**:
    *   `call_model`: This node is responsible for invoking the LLM. It takes the current `AgentState` (messages) as input, calls the `llm_with_tools` (LLM bound with the mathematical tools), and updates the state with the LLM's response. The LLM is configured to use the `llama3-8b-8192` model.
    *   `call_tool`: This node executes the detected mathematical tool. If the LLM's response indicates a tool call, this node extracts the tool name and arguments, then calls the corresponding Python function (`plus`, `subtract`, `multiply`, `divide`). It updates the state with the tool's output.
*   **Conditional Edge (`tool_router`)**:
    *   The `tool_router` function acts as the decision-maker for the graph. After the `call_model` node processes a message, the `tool_router` examines the last message in the `AgentState`.
    *   If the LLM's response contains `tool_calls` (indicating a mathematical operation), the router directs the flow to the `call_tool` node.
    *   If there are no `tool_calls`, the query is considered general, and the flow ends (`__end__`), meaning the LLM's general response is the final answer.
*   **Edges**:
    *   **Entry Point**: The graph always starts at the `call_model` node (`workflow.set_entry_point("call_model")`).
    *   **Model to Tool/End**: From `call_model`, a conditional edge (`add_conditional_edges`) uses `tool_router` to transition to either `call_tool` (if a tool is called) or `END` (if the LLM provides a direct answer).
    *   **Tool to Model**: After a tool is executed by `call_tool`, the flow returns to `call_model` (`workflow.add_edge("call_tool", "call_model")`). This allows the LLM to summarize the tool's output or continue the conversation if further steps are needed.

## Setup and Installation

1.  **Clone the repository**:

    ```bash
    git clone <repository_url>
    cd Day-10/Math_Agent
    ```

2.  **Create a virtual environment** (recommended):

    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:

    *   On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    *   On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Set up Groq API Key**:

    Create a `.env` file in the `Day-10/Math_Agent` directory and add your Groq API key:

    ```
    GROQ_API_KEY="your_groq_api_key_here"
    ```

    You can obtain a Groq API key from [Groq Console](https://console.groq.com/).

## How to Run

Execute the `agent.py` script:

```bash
python agent.py
```

The script will run a series of predefined test queries, demonstrating both mathematical and general question-answering capabilities.

## Code Explanation

### `agent.py`

*   **Imports**: Essential modules from `os`, `dotenv`, `langchain_groq`, `langchain_core.pydantic_v1`, `langchain_core.tools`, `langchain_core.runnables`, `langgraph.graph`, `typing`, and `operator` are imported.
*   **Environment Variables**: `load_dotenv()` loads the API key from the `.env` file.
*   **LLM Initialization**: `ChatGroq` is initialized with `model="llama3-8b-8192"` and `temperature=0` for consistent responses.
*   **Mathematical Tools**: `plus`, `subtract`, `multiply`, `divide` are defined using the `@tool` decorator. They include type hints for `a` and `b` as `Union[int, float]` and return `Union[int, float]`. The `divide` function includes error handling for division by zero.
*   **Tool Binding**: The mathematical tools are bound to the `llm` instance using `llm.bind_tools(tools)`, making them available for the LLM to invoke based on user queries.
*   **AgentState**: Defines the structure of the state that passes through the graph, primarily a list of `BaseMessage` objects.
*   **`call_tool(state)` Function**: This node extracts `tool_calls` from the last message in the state, identifies the tool name and arguments, and invokes the corresponding Python function. The result is then added back to the state as an `AIMessage`.
*   **`call_model(state)` Function**: This node takes the current conversation `messages` from the state, invokes the `llm_with_tools`, and appends the LLM's response to the messages in the state.
*   **`tool_router(state)` Function**: This crucial function determines the next step in the graph. If the `last_message.tool_calls` list is not empty, it means the LLM has decided to use a tool, and the function returns `"call_tool"`. Otherwise, it returns `"__end__"` (or `"call_model"` if the LLM should continue processing the message directly).
*   **Graph Definition**: The `StateGraph` is built by adding nodes and defining the entry point and conditional edges. The `add_conditional_edges` method is used with `tool_router` to dynamically transition between nodes based on the LLM's intent.
*   **Execution**: The `if __name__ == "__main__":` block contains example queries for both mathematical operations and general questions, demonstrating the agent's capabilities. 