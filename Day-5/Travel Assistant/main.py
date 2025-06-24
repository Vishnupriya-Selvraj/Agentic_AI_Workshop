import streamlit as st
import os
from dotenv import load_dotenv
from agent import TravelAssistant

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Travel Assistant AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)
 
# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background-color: #1f77b4;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-size: 1.1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #0d5aa7;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Travel Assistant AI ✈️</h1>', unsafe_allow_html=True)
    st.markdown("Get weather forecasts and discover amazing attractions for your next destination!")
    
    # Sidebar for API configuration
    with st.sidebar:
        st.header("🔧 Configuration")
        
        weather_api_key = st.text_input(
            "Weather API Key",
            value=os.getenv("WEATHER_API_KEY", ""),
            type="password",
            help="Get free key from weatherapi.com"
        )
        
        google_api_key = st.text_input(
            "Google Gemini API Key",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Get free key from ai.google.dev"
        )
        
        st.markdown("---")
        st.markdown("### 📚 How to get API keys:")
        st.markdown("1. **Weather API**: Sign up at [weatherapi.com](https://weatherapi.com)")
        st.markdown("2. **Google AI**: Get key at [ai.google.dev](https://ai.google.dev)")
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    # Initialize destination from session state if available
    default_destination = st.session_state.get('selected_destination', '')
    
    with col1:
        st.subheader("🗺️ Enter Your Destination")
        destination = st.text_input(
            "Where would you like to travel?",
            value=default_destination,
            placeholder="e.g., Paris, Tokyo, New York, London...",
            help="Enter any city or location worldwide"
        )
        
        # Clear the session state after using it
        if 'selected_destination' in st.session_state:
            del st.session_state.selected_destination
        
        if st.button("🚀 Get Travel Information", type="primary"):
            if not destination:
                st.error("Please enter a destination!")
            elif not weather_api_key or not google_api_key:
                st.error("Please provide both API keys in the sidebar!")
            else:
                with st.spinner(f"🔍 Gathering information for {destination}..."):
                    try:
                        # Initialize travel assistant
                        assistant = TravelAssistant(weather_api_key, google_api_key)
                        
                        # Get travel advice
                        result = assistant.get_travel_advice(destination)
                        
                        # Display result
                        st.success("✅ Information retrieved successfully!")
                        st.markdown("---")
                        st.markdown(result)
                        
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        st.info("💡 Make sure your API keys are correct and you have internet connection.")
    
    with col2:
        st.subheader("🎯 Quick Destinations")
        popular_destinations = [
            "Paris, France",
            "Tokyo, Japan",
            "London, UK",
            "New York, USA",
            "Rome, Italy",
            "Barcelona, Spain",
            "Sydney, Australia",
            "Bangkok, Thailand"
        ]
        
        for dest in popular_destinations:
            if st.button(dest, key=dest):
                # Set the destination in session state and rerun
                st.session_state.selected_destination = dest
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🌟 Travel Assistant AI - Your intelligent travel companion</p>
        <p>Made with ❤️ using Streamlit, LangChain, and Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()