import os
import requests
from datetime import datetime
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Optional


class WeatherTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def get_weather_forecast(self, location: str) -> str:
        """Get current weather and 3-day forecast for a location."""
        try:
            base_url = "http://api.weatherapi.com/v1"
            
            # Current weather
            current_url = f"{base_url}/current.json"
            current_params = {
                'key': self.api_key,
                'q': location,
                'aqi': 'no'
            }
            
            current_response = requests.get(current_url, params=current_params)
            current_response.raise_for_status()
            current_data = current_response.json()
            
            # 3-day forecast
            forecast_url = f"{base_url}/forecast.json"
            forecast_params = {
                'key': self.api_key,
                'q': location,
                'days': 3,
                'aqi': 'no'
            }
            
            forecast_response = requests.get(forecast_url, params=forecast_params)
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # Format response
            location_info = current_data['location']
            current = current_data['current']
            
            result = f"""🌤️ Weather for {location_info['name']}, {location_info['country']}:

📍 CURRENT CONDITIONS:
- Temperature: {current['temp_c']}°C ({current['temp_f']}°F)
- Condition: {current['condition']['text']}
- Feels like: {current['feelslike_c']}°C
- Humidity: {current['humidity']}%
- Wind: {current['wind_kph']} km/h {current['wind_dir']}

📅 3-DAY FORECAST:"""
            
            for day in forecast_data['forecast']['forecastday']:
                date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A, %B %d')
                day_data = day['day']
                result += f"""
{date}:
  🌡️ High: {day_data['maxtemp_c']}°C
  🌡️ Low: {day_data['mintemp_c']}°C
  ☁️ {day_data['condition']['text']}
  🌧️ Rain chance: {day_data['daily_chance_of_rain']}%"""
            
            return result
            
        except Exception as e:
            return f"❌ Weather error: {str(e)}"


class AttractionsSearchTool:
    def __init__(self):
        self.search_tool = DuckDuckGoSearchRun()
    
    def search_attractions(self, location: str) -> str:
        """Search for top tourist attractions in a location."""
        try:
            query = f"top tourist attractions things to do {location} travel guide"
            results = self.search_tool.run(query)
            
            return f"""🏛️ TOP ATTRACTIONS IN {location.upper()}:

{results}

ℹ️ Note: Verify current opening hours and prices before visiting."""
            
        except Exception as e:
            return f"❌ Search error: {str(e)}"


# Create standalone tool functions that can be used by LangChain
def create_weather_tool(api_key: str):
    """Create a weather tool function."""
    weather_instance = WeatherTool(api_key)
    
    @tool
    def get_weather_forecast(location: str) -> str:
        """Get current weather and 3-day forecast for a location."""
        return weather_instance.get_weather_forecast(location)
    
    return get_weather_forecast


def create_attractions_tool():
    """Create an attractions search tool function."""
    attractions_instance = AttractionsSearchTool()
    
    @tool
    def search_attractions(location: str) -> str:
        """Search for top tourist attractions in a location."""
        return attractions_instance.search_attractions(location)
    
    return search_attractions