# 🔧 Groq LLM Setup Guide

This guide will help you set up Groq LLM for the Math Agent.

## 🚀 Quick Setup

### Step 1: Get a Groq API Key

1. Go to [Groq Console](https://console.groq.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the API key (it starts with `gsk_`)

### Step 2: Install Dependencies

```bash
cd Math_Agent
pip install langchain-groq
```

### Step 3: Configure Environment

Create a `.env` file in the Math_Agent directory:

```env
GROQ_API_KEY=gsk_your_api_key_here
```

Replace `gsk_your_api_key_here` with your actual Groq API key.

### Step 4: Test the Setup

Run the setup script:

```bash
python setup_groq.py
```

Or test directly:

```bash
python simple_interactive_agent.py
```

## 🔍 Troubleshooting

### Common Issues

#### 1. "No module named 'langchain_groq'"

**Solution:**

```bash
pip install langchain-groq
```

#### 2. "GROQ_API_KEY not found"

**Solution:**

- Create a `.env` file in the Math_Agent directory
- Add your API key: `GROQ_API_KEY=gsk_your_key_here`

#### 3. "Error connecting to Groq"

**Solutions:**

- Check your internet connection
- Verify your API key is correct
- Ensure you have sufficient credits in your Groq account
- Try using a different model (e.g., `mixtral-8x7b-32768`)

#### 4. Python Environment Issues

**Solution:**
Use the simplified agent that works with any environment:

```bash
python simple_interactive_agent.py
```

## 📋 Available Models

Groq offers several models. You can change the model in the agent files:

### Fast Models (Recommended)

- `llama3-8b-8192` - Fast and efficient
- `mixtral-8x7b-32768` - Good balance of speed and quality

### High-Quality Models

- `llama3-70b-8192` - Higher quality but slower
- `gemma2-9b-it` - Good for instruction following

### Example Model Configuration

```python
# In agent.py, interactive_agent.py, or web_agent.py
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)
```

## 🎯 Usage Examples

### Interactive Mode

```bash
python simple_interactive_agent.py
```

### Web Interface

```bash
python web_agent.py
```

### Test Script

```bash
python agent.py
```

## 💡 Tips for Best Performance

1. **Use Fast Models**: `llama3-8b-8192` or `mixtral-8x7b-32768` for quick responses
2. **Set Temperature to 0**: For consistent, deterministic responses
3. **Monitor Usage**: Check your Groq console for usage and costs
4. **Error Handling**: The agent falls back to MockLLM if Groq fails

## 🔄 Switching Between LLM Providers

### To OpenAI:

```python
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
```

### To Gemini:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
```

### To MockLLM (for testing):

```python
# The agent automatically falls back to MockLLM if other LLMs fail
```

## 📊 Cost Comparison

| Provider | Model          | Speed     | Cost per 1M tokens |
| -------- | -------------- | --------- | ------------------ |
| Groq     | llama3-8b-8192 | Very Fast | ~$0.05             |
| OpenAI   | gpt-3.5-turbo  | Fast      | ~$0.50             |
| Google   | gemini-pro     | Medium    | ~$0.15             |

## 🛠️ Advanced Configuration

### Custom Model Parameters

```python
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0,
    max_tokens=1000,
    top_p=1.0
)
```

### Environment Variables

You can set additional environment variables:

```env
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=llama3-8b-8192
GROQ_TEMPERATURE=0
```

### Error Handling

The agent includes robust error handling:

```python
try:
    from langchain_groq import ChatGroq
    llm = ChatGroq(model="llama3-8b-8192", temperature=0)
except Exception as e:
    print(f"Groq error: {e}")
    # Fall back to MockLLM
```

## 🎉 Success Indicators

When Groq is working correctly, you should see:

```
🔧 Initializing LLM...
✅ Successfully connected to Groq LLM
🧮 LangGraph Math Agent - Interactive Mode
```

## 📞 Support

If you encounter issues:

1. **Check the console output** for specific error messages
2. **Verify your API key** is correct and active
3. **Test your internet connection**
4. **Check your Groq account** for remaining credits
5. **Try the simplified agent** as a fallback

## 🔗 Useful Links

- [Groq Console](https://console.groq.com/)
- [Groq Documentation](https://console.groq.com/docs)
- [LangChain Groq Integration](https://python.langchain.com/docs/integrations/llms/groq)
- [API Key Management](https://console.groq.com/keys)

---

**Happy coding! 🚀**
