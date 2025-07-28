import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List, Union
import operator
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
import json
import re

# Load environment variables
load_dotenv()

# Initialize LLM with better error handling
def initialize_llm():
    """Initialize LLM with Groq if available, otherwise use MockLLM."""
    print("🔧 Initializing LLM...")
    
    # Check if API key exists
    groq_api_key = os.getenv("GROQ_API_KEY")
    if not groq_api_key:
        print("⚠️  GROQ_API_KEY not found in .env file")
        print("📝 To use Groq, create a .env file with: GROQ_API_KEY=your_api_key_here")
        print("🔗 Get your API key from: https://console.groq.com/")
        return create_mock_llm()
    
    print(f"✅ Found Groq API key: {groq_api_key[:10]}...")
    
    # Try to use Groq
    try:
        import sys
        print(f"🔍 Python path: {sys.executable}")
        print(f"🔍 Python version: {sys.version}")
        
        from langchain_groq import ChatGroq
        print("✅ Successfully imported langchain_groq")
        
        llm = ChatGroq(model="llama3-8b-8192", temperature=0)
        print("✅ Successfully connected to Groq LLM")
        
        # Test the connection
        test_response = llm.invoke([HumanMessage(content="Hello!")])
        print(f"✅ Groq test response: {test_response.content[:50]}...")
        
        return llm
        
    except ImportError as e:
        print(f"❌ langchain-groq import error: {e}")
        print("📦 Install with: pip install langchain-groq")
        print("🔧 Falling back to MockLLM...")
        return create_mock_llm()
        
    except Exception as e:
        print(f"❌ Error connecting to Groq: {str(e)}")
        print("🔧 Falling back to MockLLM...")
        return create_mock_llm()

def create_mock_llm():
    """Create a MockLLM for fallback."""
    class MockLLM:
        def invoke(self, messages):
            last_message = messages[-1].content if messages else ""
            if "capital" in last_message.lower():
                return AIMessage(content="The capital of France is Paris.")
            elif "language model" in last_message.lower():
                return AIMessage(content="Large Language Models (LLMs) are AI systems trained on vast amounts of text data to understand and generate human-like text.")
            elif "artificial intelligence" in last_message.lower() or "ai" in last_message.lower():
                return AIMessage(content="Artificial Intelligence (AI) is a branch of computer science that aims to create systems capable of performing tasks that typically require human intelligence.")
            elif "weather" in last_message.lower():
                return AIMessage(content="I don't have access to real-time weather data, but I can help with mathematical calculations and general questions!")
            elif "hello" in last_message.lower() or "hi" in last_message.lower():
                return AIMessage(content="Hello! I'm your Math Agent. I can help with mathematical operations and general questions. What would you like to know?")
            elif "groq" in last_message.lower():
                return AIMessage(content="Groq is a fast LLM provider. To use it with this agent, install langchain-groq and set your GROQ_API_KEY in a .env file.")
            elif "langgraph" in last_message.lower():
                return AIMessage(content="LangGraph is a framework for building stateful, multi-actor applications with LLMs. It's great for creating complex workflows and agent systems.")
            else:
                return AIMessage(content="I can help with general questions and mathematical operations. Please ask me anything!")
    
    return MockLLM()

llm = initialize_llm()

# 1. Define Custom Functions (Mathematical Tools)
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

# 2. Integrate LLM with Tools
tools = [plus, subtract, multiply, divide]

# 3. Math Parser for detecting mathematical queries
def parse_math_expression(text: str):
    """Parse simple mathematical expressions from text."""
    # Extract numbers and operations
    numbers = re.findall(r'\d+', text)
    operations = []
    
    text_lower = text.lower()
    
    if 'plus' in text_lower or '+' in text:
        operations.append('plus')
    elif 'minus' in text_lower or 'subtract' in text_lower or '-' in text:
        operations.append('subtract')
    elif 'multiply' in text_lower or '*' in text or 'times' in text_lower:
        operations.append('multiply')
    elif 'divide' in text_lower or '/' in text:
        operations.append('divide')
    
    return numbers, operations

def execute_math_operation(operation: str, numbers: List[Union[int, float]]) -> Union[int, float]:
    """Execute mathematical operation on numbers."""
    if len(numbers) < 2:
        return numbers[0] if numbers else 0
    
    a, b = float(numbers[0]), float(numbers[1])
    
    if operation == 'plus':
        return a + b
    elif operation == 'subtract':
        return a - b
    elif operation == 'multiply':
        return a * b
    elif operation == 'divide':
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

# 4. Create LangGraph - Define Agent State
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]

# Define the nodes for the graph
def call_tool(state: AgentState):
    """Node for executing mathematical tools."""
    # Get the original user message (first message in the conversation)
    if len(state["messages"]) > 0:
        original_message = state["messages"][0]
        content = original_message.content if hasattr(original_message, 'content') else str(original_message)
    else:
        return {"messages": [AIMessage(content="No message to process.")]}
    
    # Parse the mathematical expression
    numbers, operations = parse_math_expression(content)
    
    if not operations:
        return {"messages": [AIMessage(content="I can help with basic math operations: addition, subtraction, multiplication, and division. Please provide a mathematical expression.")]}
    
    try:
        result = execute_math_operation(operations[0], numbers)
        return {"messages": [AIMessage(content=f"The result is: {result}")]}
    except Exception as e:
        return {"messages": [AIMessage(content=f"Error: {str(e)}")]}

def call_model(state: AgentState):
    """Node for calling the LLM for general questions."""
    messages = state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

# 5. Conditional Edges - Tool Router
def tool_router(state: AgentState):
    """Router to decide whether to use tools or LLM."""
    # Get the original user message (first message in the conversation)
    if len(state["messages"]) > 0:
        original_message = state["messages"][0]
        content = original_message.content if hasattr(original_message, 'content') else str(original_message)
    else:
        return "__end__"
    
    # Check if it's a mathematical expression
    numbers, operations = parse_math_expression(content)
    
    if operations and numbers:
        return "call_tool"
    else:
        return "__end__"

# 6. Build the LangGraph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("call_model", call_model)
workflow.add_node("call_tool", call_tool)

# Set entry point
workflow.set_entry_point("call_model")

# Add conditional edges
workflow.add_conditional_edges(
    "call_model",
    tool_router,
    {"call_tool": "call_tool", "__end__": END}
)

# Add edge from tool back to end
workflow.add_edge("call_tool", END)

# Compile the graph
app = workflow.compile()

def run_interactive_agent():
    """Run the agent in interactive mode."""
    print("🧮 LangGraph Math Agent - Interactive Mode")
    print("=" * 60)
    print("This agent can handle both mathematical operations and general questions.")
    print("Examples:")
    print("  Math: 'What is 5 plus 3?', 'Multiply 6 by 9', 'Divide 100 by 4'")
    print("  General: 'What is the capital of France?', 'Tell me about AI'")
    print("  Type 'quit' or 'exit' to stop")
    print("=" * 60)
    
    while True:
        try:
            # Get user input
            user_input = input("\n❓ You: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("\n👋 Goodbye! Thanks for using the Math Agent!")
                break
            
            # Skip empty input
            if not user_input:
                continue
            
            # Process the query
            print("🤖 Agent: ", end="", flush=True)
            
            # Run the agent
            for s in app.stream({"messages": [HumanMessage(content=user_input)]}):
                if "__end__" not in s:
                    for node_name, node_output in s.items():
                        if node_name != "__end__":
                            response = node_output['messages'][-1].content
                            print(response)
                            break
                else:
                    # Handle the final response
                    for node_name, node_output in s.items():
                        if node_name == "__end__":
                            if "messages" in node_output and node_output["messages"]:
                                response = node_output["messages"][-1].content
                                print(response)
                            break
                    
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Thanks for using the Math Agent!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            print("Please try again with a different query.")

if __name__ == "__main__":
    run_interactive_agent() 