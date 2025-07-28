#!/usr/bin/env python3
"""
Simple test script to verify Groq connection
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_groq():
    """Test Groq connection."""
    print("🧪 Testing Groq Connection...")
    
    # Check if API key exists
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in .env file")
        return False
    
    print(f"✅ Found API key: {api_key[:10]}...")
    
    # Try to import and use Groq
    try:
        from langchain_groq import ChatGroq
        from langchain_core.messages import HumanMessage
        
        print("✅ Successfully imported langchain_groq")
        
        # Initialize Groq
        llm = ChatGroq(model="llama3-8b-8192", temperature=0)
        print("✅ Successfully initialized Groq LLM")
        
        # Test with a simple query
        response = llm.invoke([HumanMessage(content="Hello! What is 2+2?")])
        print(f"✅ Groq response: {response.content}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: pip install langchain-groq")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

if __name__ == "__main__":
    success = test_groq()
    if success:
        print("\n🎉 Groq is working! You can now use it with the Math Agent.")
    else:
        print("\n❌ Groq setup failed. Check the error messages above.") 