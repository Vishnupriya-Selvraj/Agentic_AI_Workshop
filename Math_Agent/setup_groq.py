#!/usr/bin/env python3
"""
Setup script for Groq LLM integration
"""

import os
import getpass
from pathlib import Path

def setup_groq():
    """Setup Groq API key and install dependencies."""
    print("🚀 Setting up Groq LLM for Math Agent")
    print("=" * 50)
    
    # Check if .env file exists
    env_file = Path(".env")
    
    if env_file.exists():
        print("📁 Found existing .env file")
        with open(env_file, 'r') as f:
            content = f.read()
            if "GROQ_API_KEY" in content:
                print("✅ GROQ_API_KEY already configured")
                return True
    else:
        print("📝 Creating new .env file")
    
    # Get API key from user
    print("\n🔑 Please enter your Groq API key:")
    print("   You can get one from: https://console.groq.com/")
    api_key = getpass.getpass("Groq API Key: ").strip()
    
    if not api_key:
        print("❌ No API key provided. Setup cancelled.")
        return False
    
    # Write to .env file
    with open(env_file, 'a') as f:
        f.write(f"\nGROQ_API_KEY={api_key}\n")
    
    print("✅ API key saved to .env file")
    
    # Install dependencies
    print("\n📦 Installing dependencies...")
    try:
        import subprocess
        subprocess.check_call(["pip", "install", "langchain-groq>=0.3.0"])
        print("✅ Dependencies installed successfully")
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    
    print("\n🎉 Setup complete!")
    print("You can now run:")
    print("  python interactive_agent.py  # For interactive mode")
    print("  python web_agent.py          # For web interface")
    
    return True

def test_groq_connection():
    """Test the Groq connection."""
    print("\n🧪 Testing Groq connection...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from langchain_groq import ChatGroq
        llm = ChatGroq(model="llama3-8b-8192", temperature=0)
        
        # Test with a simple query
        from langchain_core.messages import HumanMessage
        response = llm.invoke([HumanMessage(content="Hello!")])
        
        print("✅ Groq connection successful!")
        print(f"🤖 Response: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Groq connection failed: {e}")
        print("🔧 Please check your API key and internet connection")
        return False

if __name__ == "__main__":
    if setup_groq():
        test_groq_connection()
    else:
        print("\n❌ Setup failed. Please try again.") 