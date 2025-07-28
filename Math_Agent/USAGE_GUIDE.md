# 🚀 Dynamic Usage Guide - LangGraph Math Agent

This guide shows you how to use the Math Agent dynamically in different ways.

## 📋 Available Interfaces

### 1. 🖥️ **Interactive Command Line Interface**

Run the agent in an interactive terminal session where you can type queries and get responses in real-time.

### 2. 🌐 **Web Interface**

Access the agent through a beautiful web interface with a modern chat UI.

### 3. 📝 **Script Mode**

Run predefined tests to verify the agent's functionality.

## 🖥️ Interactive Command Line Interface

### How to Use:

```bash
cd Math_Agent
python interactive_agent.py
```

### Features:

- **Real-time interaction**: Type queries and get immediate responses
- **Exit commands**: Type `quit`, `exit`, `bye`, or `q` to stop
- **Error handling**: Graceful error handling for invalid inputs
- **Examples provided**: Shows examples of what you can ask

### Example Session:

```
🧮 LangGraph Math Agent - Interactive Mode
============================================================
This agent can handle both mathematical operations and general questions.
Examples:
  Math: 'What is 5 plus 3?', 'Multiply 6 by 9', 'Divide 100 by 4'
  General: 'What is the capital of France?', 'Tell me about AI'
  Type 'quit' or 'exit' to stop
============================================================

❓ You: What is 15 plus 8?
🤖 Agent: The result is: 23.0

❓ You: What is the capital of France?
🤖 Agent: The capital of France is Paris.

❓ You: quit
👋 Goodbye! Thanks for using the Math Agent!
```

## 🌐 Web Interface

### How to Use:

```bash
cd Math_Agent
pip install flask  # If not already installed
python web_agent.py
```

Then open your browser and go to: `http://localhost:5000`

### Features:

- **Beautiful UI**: Modern, responsive web interface
- **Clickable examples**: Click on example queries to try them
- **Real-time chat**: Send messages and get instant responses
- **Mobile-friendly**: Works on desktop and mobile devices
- **Visual feedback**: Loading indicators and smooth animations

### Web Interface Features:

- **Mathematical Operations**: Addition, subtraction, multiplication, division
- **General Questions**: Ask about geography, technology, AI, etc.
- **Example Queries**: Click on examples to try them instantly
- **Responsive Design**: Works on all screen sizes
- **Modern UI**: Beautiful gradient design with smooth interactions

## 📝 Script Mode (Original)

### How to Use:

```bash
cd Math_Agent
python agent.py
```

### Features:

- **Predefined tests**: Runs through a series of test queries
- **Demonstration**: Shows both mathematical and general query handling
- **Validation**: Verifies that all features work correctly

## 🔧 Configuration Options

### LLM Integration

The agent supports multiple LLM providers. To use a specific one, edit the `agent.py`, `interactive_agent.py`, or `web_agent.py` file:

#### OpenAI:

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
```

#### Groq:

```python
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama3-8b-8192", temperature=0)
```

#### Gemini:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
```

### Environment Variables

Create a `.env` file in the Math_Agent directory:

```env
# For OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# For Groq
GROQ_API_KEY=your_groq_api_key_here

# For Gemini
GOOGLE_API_KEY=your_google_api_key_here
```

## 📊 Supported Operations

### Mathematical Operations:

- **Addition**: "What is 5 plus 3?", "15 + 8"
- **Subtraction**: "Subtract 10 from 7", "Calculate 20 - 5"
- **Multiplication**: "Multiply 6 by 9", "What is 4 \* 7?"
- **Division**: "Divide 100 by 4", "Divide 50 by 2"

### General Questions:

- **Geography**: "What is the capital of France?"
- **Technology**: "Tell me about artificial intelligence"
- **AI/ML**: "What are large language models?"
- **Greetings**: "Hello!", "Hi there"

## 🎯 Usage Examples

### Interactive Mode Examples:

```bash
# Start interactive mode
python interactive_agent.py

# Then type queries like:
What is 25 plus 17?
Multiply 8 by 9
Divide 100 by 5
What is the capital of Japan?
Tell me about machine learning
Hello!
quit
```

### Web Interface Examples:

1. Start the web server: `python web_agent.py`
2. Open browser: `http://localhost:5000`
3. Click on example queries or type your own
4. Enjoy the interactive chat experience!

## 🚨 Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are installed:

   ```bash
   pip install -r requirements.txt
   ```

2. **Port Already in Use**: If port 5000 is busy, change it in `web_agent.py`:

   ```python
   flask_app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
   ```

3. **LLM API Errors**: Check your API keys and internet connection

4. **Flask Not Found**: Install Flask:
   ```bash
   pip install flask
   ```

### Getting Help:

- Check the console output for error messages
- Ensure all dependencies are installed
- Verify your API keys are correct
- Check your internet connection

## 🎨 Customization

### Adding New Mathematical Operations:

1. Add a new tool function in the agent files
2. Update the `parse_math_expression` function
3. Add the operation to the `execute_math_operation` function

### Adding New LLM Responses:

1. Modify the `MockLLM` class or use a real LLM
2. Add new response patterns based on keywords

### Styling the Web Interface:

1. Edit the CSS in the `html_template` variable in `web_agent.py`
2. Customize colors, fonts, and layout

## 📈 Performance Tips

1. **Use Real LLM**: Replace the MockLLM with a real LLM for better responses
2. **Optimize Parsing**: Improve the math parser for more complex expressions
3. **Add Caching**: Cache common responses for faster performance
4. **Error Handling**: Add more robust error handling for edge cases

## 🎉 Enjoy Your Dynamic Math Agent!

Choose the interface that works best for you:

- **Quick testing**: Use script mode (`python agent.py`)
- **Interactive chat**: Use command line mode (`python interactive_agent.py`)
- **Beautiful UI**: Use web interface (`python web_agent.py`)

The agent is designed to be flexible and user-friendly, so you can interact with it in the way that feels most natural to you!
