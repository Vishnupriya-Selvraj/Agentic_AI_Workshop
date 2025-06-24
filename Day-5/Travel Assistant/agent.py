import os
from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import create_weather_tool, create_attractions_tool


class TravelAssistant:
    def __init__(self, weather_api_key: str, google_api_key: str):
        # Set up LLM
        os.environ["GOOGLE_API_KEY"] = google_api_key
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7
        )
        
        # Create tools using the factory functions
        weather_tool = create_weather_tool(weather_api_key)
        attractions_tool = create_attractions_tool()
        
        self.tools = [
            weather_tool,
            attractions_tool
        ]
        
        # Create agent using initialize_agent (compatible with older versions)
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,  # Enable verbose to see what's happening
            handle_parsing_errors=True,
            max_iterations=5,  # Increased from 3
            max_execution_time=120,  # Add execution time limit (2 minutes)
            early_stopping_method="generate",  # Stop gracefully when needed
            agent_kwargs={
                'prefix': """🌍 You are a Travel Assistant AI!

Help travelers by providing:
1. 🌤️ Weather information and forecasts
2. 🏛️ Tourist attractions and places to visit  
3. 💡 Travel advice based on conditions

Always:
✅ Use both tools for complete information
✅ Give weather-based recommendations
✅ Suggest appropriate clothing
✅ Be enthusiastic and helpful
✅ Format with emojis and clear sections

Be friendly and make travel planning exciting! 🎉

IMPORTANT: After gathering weather and attractions information, provide a final answer immediately.

You have access to the following tools:"""
            }
        )
    
    def get_travel_advice(self, destination: str) -> str:
        try:
            input_text = f"""I want to travel to {destination}. 
            Please provide current weather forecast and top attractions. 
            Give practical travel advice based on weather conditions."""
            
            print(f"🔍 Processing request for: {destination}")
            result = self.agent.run(input_text)
            print(f"✅ Successfully completed request for: {destination}")
            return result
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            print(f"🚨 Error occurred: {error_msg}")
            return error_msg