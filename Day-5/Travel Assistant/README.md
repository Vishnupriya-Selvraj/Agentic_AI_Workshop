# 🌍 Travel Assistant AI ✈️

An intelligent travel companion that provides real-time weather forecasts and discovers amazing attractions for your next destination using AI-powered agents.

## 🚀 Features

- **🌤️ Real-time Weather Forecasts**: Get current conditions and 3-day forecasts for any destination
- **🏛️ Tourist Attractions Discovery**: Find top attractions and things to do using intelligent web search
- **💡 Personalized Travel Advice**: Weather-based recommendations and clothing suggestions
- **🎯 Quick Destination Selection**: Pre-populated popular destinations for easy access
- **🤖 AI-Powered Agent**: Uses Google's Gemini AI with LangChain for intelligent responses
- **📱 Beautiful UI**: Modern Streamlit interface with responsive design

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Framework**: LangChain
- **LLM**: Google Gemini 1.5 Flash
- **Weather API**: WeatherAPI.com
- **Search Engine**: DuckDuckGo Search
- **Language**: Python 3.8+

## 📋 Prerequisites

Before running the application, you'll need to obtain API keys:

### 1. Weather API Key
- Visit [WeatherAPI.com](https://weatherapi.com)
- Create a free account
- Get your API key from the dashboard
- Free tier includes: 1 million calls/month

### 2. Google Gemini API Key
- Visit [Google AI Studio](https://ai.google.dev)
- Create a Google account or sign in
- Generate an API key
- Free tier includes: 15 requests/minute, 1 million tokens/minute

## 🔧 Installation

### 1. Clone the Repository
```bash
git clone <https://github.com/Vishnupriya-Selvraj/Agentic_AI_Workshop>
cd travel-assistant-ai
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Setup
Create a `.env` file in the root directory:
```bash
WEATHER_API_KEY=your_weather_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

## 🚀 Usage

### 1. Start the Application
```bash
streamlit run main.py
```

### 2. Access the Web Interface
- Open your browser and go to `http://localhost:8501`
- The application will automatically open in your default browser

### 3. Using the Application

#### Method 1: Manual Input
1. Enter your destination in the text input field
2. Click "🚀 Get Travel Information"
3. Wait for the AI agent to gather weather and attraction data

#### Method 2: Quick Destinations
1. Click on any of the pre-populated destination buttons
2. The destination will be automatically filled in the input field
3. Click "🚀 Get Travel Information"

#### Method 3: API Key Configuration
- If you haven't set up the `.env` file, you can enter API keys directly in the sidebar
- The keys will be used for the current session only

## 📁 Project Structure

```
travel-assistant-ai/
│
├── main.py                 # Streamlit web interface
├── agent.py                # LangChain agent implementation
├── tools.py                # Weather and attractions search tools
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── README.md              # This file
└── venv/                  # Virtual environment (created during setup)
```

## 🔧 Configuration

### Environment Variables
```bash
# Required API Keys
WEATHER_API_KEY=your_weather_api_key
GOOGLE_API_KEY=your_google_gemini_api_key

# Optional Settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### Agent Configuration
You can modify the agent behavior in `agent.py`:

```python
# Model Selection
model="gemini-1.5-flash"  # Fast and efficient
# model="gemini-1.5-pro"   # More powerful for complex tasks
# model="gemini-1.0-pro"   # Legacy but stable

# Agent Parameters
max_iterations=5           # Maximum reasoning steps
max_execution_time=120     # Time limit in seconds
temperature=0.7           # Response creativity (0.0-1.0)
```

## 🛠️ Troubleshooting

### Common Issues

#### 1. API Key Errors
```
❌ Error: Invalid API key
```
**Solution**: Verify your API keys are correct and active

#### 2. Model Not Found
```
NotFound: 404 models/gemini-pro is not found
```
**Solution**: Update to a supported model (gemini-1.5-flash)

#### 3. Agent Timeout
```
Agent stopped due to iteration limit or time limit
```
**Solution**: The agent configuration has been optimized, but you can:
- Increase `max_iterations` in `agent.py`
- Increase `max_execution_time` 
- Check your internet connection

#### 4. Installation Issues
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Debug Mode
Enable verbose logging by setting `verbose=True` in `agent.py` to see detailed agent reasoning steps.

## 🎯 Popular Destinations

The app includes quick-access buttons for popular destinations:
- 🇫🇷 Paris, France
- 🇯🇵 Tokyo, Japan
- 🇬🇧 London, UK
- 🇺🇸 New York, USA
- 🇮🇹 Rome, Italy
- 🇪🇸 Barcelona, Spain
- 🇦🇺 Sydney, Australia
- 🇹🇭 Bangkok, Thailand

## 📊 API Limits

### WeatherAPI.com (Free Tier)
- 1,000,000 calls/month
- 3-day forecast included
- No credit card required

### Google Gemini (Free Tier)
- 15 requests/minute
- 1 million tokens/minute
- 1,500 requests/day

## 🔐 Security

- API keys are stored securely in environment variables
- Keys entered in the UI are not stored permanently
- All API calls are made server-side
- No user data is collected or stored

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your API keys as secrets in the dashboard
4. Deploy with one click

### Local Network Access
```bash
streamlit run main.py --server.address 0.0.0.0
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📝 Dependencies

```txt
streamlit==1.28.0         # Web framework
requests==2.31.0          # HTTP requests
langchain==0.1.0          # AI agent framework
langchain-community==0.0.20   # Community tools
langchain-google-genai==0.0.11  # Google Gemini integration
langchain-core==0.1.0     # Core LangChain functionality
duckduckgo-search==3.9.6  # Web search capability
python-dotenv==1.0.0      # Environment variable management
```

## 🐛 Known Issues

1. **DuckDuckGo Rate Limiting**: Heavy usage may trigger rate limits
2. **Gemini API Quotas**: Free tier has daily limits
3. **Weather API Limits**: Free tier has monthly limits

## 🔄 Version History

### v1.0.0 (Current)
- Initial release
- Weather forecasting
- Attractions search
- AI-powered travel advice
- Streamlit web interface

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
1. Check the troubleshooting section above
2. Review the API documentation:
   - [WeatherAPI Docs](https://weatherapi.com/docs/)
   - [Google Gemini Docs](https://ai.google.dev/docs)
3. Create an issue in the repository

## 🌟 Acknowledgments

- **WeatherAPI.com** for reliable weather data
- **Google AI** for the powerful Gemini models
- **LangChain** for the agent framework
- **Streamlit** for the beautiful web interface
- **DuckDuckGo** for search capabilities

---

**Made with ❤️ using Streamlit, LangChain, and Google Gemini**

*Happy Travels! 🌍✈️*