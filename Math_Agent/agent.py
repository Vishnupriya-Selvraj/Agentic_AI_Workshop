import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda
# from langgraph.prebuilt import AgentExecutor
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Union
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
import json

# Load environment variables
load_dotenv()

# Set up Groq API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the Groq language model
llm = ChatGroq(model="llama3-8b-8192", temperature=0)

# 1. Define Custom Functions

@tool
def plus(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Add two numbers."""
    return operator.add(a, b)

@tool
def subtract(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Subtract two numbers."""
    return operator.sub(a, b)

@tool
def multiply(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Multiply two numbers."""
    return operator.mul(a, b)

@tool
def divide(a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
    """Divide two numbers, with error handling for division by zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return operator.truediv(a, b)

# 2. Integrate LLM (tools are bound here)
tools = [plus, subtract, multiply, divide]
llm_with_tools = llm.bind_tools(tools)

# 3. Create LangGraph - Define Agent State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# Define the nodes for the graph
def call_tool(state: AgentState):
    last_message = state["messages"][-1]
    tool_calls = last_message.tool_calls
    if not tool_calls:
        raise ValueError("No tool calls found in the last message.")
    
    # Assuming one tool call per message for simplicity
    tool_call = tool_calls[0]
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)

    if tool_name == "plus":
        result = plus.invoke(**tool_args)
    elif tool_name == "subtract":
        result = subtract.invoke(**tool_args)
    elif tool_name == "multiply":
        result = multiply.invoke(**tool_args)
    elif tool_name == "divide":
        result = divide.invoke(**tool_args)
    else:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    return {"messages": [AIMessage(content=f"The result is: {result}")]}

def call_model(state: AgentState):
    messages = state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

# 4. Conditional Edges - Tool Router
def tool_router(state: AgentState):
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "call_tool"
    else:
        return "__end__"

# Build the graph
workflow = StateGraph(AgentState)

workflow.add_node("call_model", call_model)
workflow.add_node("call_tool", call_tool)

workflow.set_entry_point("call_model")

workflow.add_conditional_edges(
    "call_model",
    tool_router,
    {"call_tool": "call_tool", "__end__": END}
)
workflow.add_edge("call_tool", END) # After tool call, directly end

app = workflow.compile()

# Test Queries
if __name__ == "__main__":
    print("Testing mathematical queries:")
    for query in ["What is 5 plus 3?", "Subtract 10 from 7.", "Multiply 6 by 9.", "Divide 100 by 4."]:
        print(f"User: {query}")
        for s in app.stream({"messages": [HumanMessage(content=query)]}):
            if "__end__" not in s:
                print(s)
        print("---")

    print("\nTesting general queries:")
    for query in ["What is the capital of France?", "Tell me about large language models."]:
        print(f"User: {query}")
        for s in app.stream({"messages": [HumanMessage(content=query)]}):
            if "__end__" not in s:
                print(s)
        print("---") 