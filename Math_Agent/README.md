# 🧮 LangGraph Math Agent

A LangGraph-based agent that seamlessly handles both mathematical operations and general questions using an LLM. This agent demonstrates the power of LangGraph in creating intelligent systems that can route between different types of processing based on the nature of the input.

## Assignment Requirements Met

✅ **LLM Integration**: Uses LLM API for general reasoning  
✅ **Custom Functions**: Four predefined mathematical functions implemented  
✅ **Mathematical Query Detection**: Automatically detects and routes math queries  
✅ **General Query Handling**: Forwards non-math queries to LLM  
✅ **LangGraph Implementation**: Complete graph-building process with tool integration  
✅ **Conditional Routing**: Appropriate graph flow using conditional edges  
✅ **Testing**: Comprehensive testing with both math and general queries

## Features

- **Mathematical Operations**: Addition, subtraction, multiplication, and division
- **Natural Language Processing**: Understands queries in plain English
- **Intelligent Routing**: Automatically routes between math tools and LLM
- **Error Handling**: Robust error handling for division by zero and invalid inputs
- **Multiple Interfaces**: Command line, interactive, and web interfaces
- **Groq LLM Integration**: Uses Groq's fast LLM for general questions
- **LangGraph Integration**: Uses LangGraph for workflow management
- **Tool-based Architecture**: Implements mathematical operations as tools
- **Conditional Routing**: Intelligently routes between LLM and mathematical tools

## Supported Operations

- **Addition**: "What is 5 plus 3?", "15 + 8"
- **Subtraction**: "Subtract 10 from 7", "Calculate 20 - 5"
- **Multiplication**: "Multiply 6 by 9", "What is 4 \* 7?"
- **Division**: "Divide 100 by 4", "Divide 50 by 2"

## 🚀 Quick Start

### 1. Setup Groq LLM (Recommended)

```bash
cd Math_Agent
python setup_groq.py
```

This will:

- Guide you through setting up your Groq API key
- Install required dependencies
- Test the connection

### 2. Manual Setup

If you prefer manual setup:

```bash
cd Math_Agent
pip install -r requirements.txt
```

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: https://console.groq.com/

## 📱 Usage Options

### Interactive Command Line Interface

```bash
python interactive_agent.py
```

### Web Interface

```bash
python web_agent.py
```

Then open: http://localhost:5000

### Script Mode (Testing)

```bash
python agent.py
```

## Architecture

### Components

1. **Mathematical Tools**: Four basic arithmetic operations implemented as tools
2. **Math Parser**: Extracts numbers and operations from natural language
3. **LangGraph Workflow**: Manages the conversation flow and tool execution
4. **State Management**: Tracks conversation state and message history
5. **Conditional Router**: Determines whether to use tools or LLM

### Workflow

1. **Input Processing**: User provides a query
2. **Routing Decision**: Agent determines if it's a mathematical or general query
3. **Tool Execution**: For math queries, appropriate mathematical tool is selected and executed
4. **LLM Processing**: For general queries, Groq LLM provides response
5. **Response**: Result is returned to the user

## Installation

```bash
git clone <repository-url>
cd Math_Agent
pip install -r requirements.txt
```

## Code Structure

```
Math_Agent/
├── agent.py              # Main agent implementation
├── interactive_agent.py  # Interactive command line interface
├── web_agent.py         # Web interface with Flask
├── setup_groq.py        # Groq setup script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── REPORT.md            # Detailed implementation report
└── USAGE_GUIDE.md      # Comprehensive usage guide
```

## Example Output

```
🧮 LangGraph Math Agent
===========================================================

📊 Testing mathematical queries:

❓ User: What is 5 plus 3?
🤖 Agent: The result is: 8.0

❓ User: Multiply 6 by 9.
🤖 Agent: The result is: 54.0

📝 Testing general queries:

❓ User: What is the capital of France?
🤖 Agent: The capital of France is Paris.

❓ User: Tell me about large language models.
🤖 Agent: Large Language Models (LLMs) are AI systems trained on vast amounts of text data...
```

## LLM Integration

The agent uses **Groq LLM** for general questions, providing:

- **Fast Responses**: Groq's optimized inference
- **High Quality**: Advanced language model capabilities
- **Reliable**: Robust API with good uptime
- **Cost Effective**: Competitive pricing for API calls

### Alternative LLM Options

You can easily switch to other LLM providers by modifying the agent files:

#### OpenAI:

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
```

#### Gemini:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
```

## Custom Mathematical Functions

The agent implements four custom mathematical functions as LangChain tools:

```python
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
```

## LangGraph Implementation

The agent uses LangGraph's `StateGraph` to manage the conversation flow:

- **State Management**: Maintains conversation history
- **Graph Nodes**: `call_model` for LLM processing, `call_tool` for mathematical operations
- **Conditional Routing**: `tool_router` determines the appropriate path
- **Tool Integration**: Mathematical functions integrated as LangChain tools

## Future Enhancements

- Support for more complex mathematical operations (exponents, roots, etc.)
- Integration with external APIs for real-time data
- Enhanced natural language processing for better query understanding
- Multi-language support
- Voice interface integration
- Advanced error handling and validation
- Performance optimization for large-scale deployments

## Contributing

Feel free to contribute by:

- Adding new mathematical operations
- Improving the natural language parser
- Enhancing the web interface
- Adding new LLM integrations
- Optimizing performance
- Adding tests and documentation

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:

- Check the `USAGE_GUIDE.md` for detailed instructions
- Review the `REPORT.md` for technical implementation details
- Ensure your Groq API key is properly configured
- Verify all dependencies are installed correctly
