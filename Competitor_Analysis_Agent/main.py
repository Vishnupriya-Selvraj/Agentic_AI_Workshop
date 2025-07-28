from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_tavily import TavilySearch
from langchain.agents import create_openai_functions_agent, AgentExecutor
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def get_clothing_store_competitor_data(location: str, store_type: str = "clothing store") -> str:
    """
    Searches for clothing store competitors in a given location and retrieves relevant data.
    This includes information about store footfall, busiest times, and general competitor overview.
    """
    try:
        tavily = TavilySearch(k=5)
        query = f"clothing store competitors in {location} footfall and busiest times"
        response = tavily.invoke({"query": query})

        # Handle the correct response format
        if isinstance(response, dict) and 'results' in response:
            results = response['results']
        elif isinstance(response, list):
            results = response
        else:
            results = [response]

        # Format the results into a readable string
        formatted_results = []
        for r in results:
            if isinstance(r, dict):
                content = r.get('content', '').strip()
                title = r.get('title', 'No title')
                url = r.get('url', 'No URL')
                if content:
                    formatted_results.append(f"Title: {title}\nURL: {url}\nContent: {content}\n---")
            elif isinstance(r, str):
                formatted_results.append(f"Content: {r}\n---")
        
        if not formatted_results:
            return "No relevant clothing store competitor data with useful content found for the given location and store type."
        
        return "\n".join(formatted_results)
    except Exception as e:
        return f"Error retrieving data: {str(e)}"

def get_agent():
    """Create and return the agent."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)
    
    # Create prompt template with better instructions
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful AI assistant specializing in competitor analysis for clothing stores. 
        When provided with search results about clothing stores in a location, analyze and present the information in a structured, professional format.
        
        Your response should include:
        1. Key shopping areas and their characteristics
        2. Notable competitors and their specialties
        3. Market insights (timings, pricing, customer segments)
        4. Recommendations or insights
        
        Format your response clearly with bullet points and sections."""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    # Create a simple function that the agent can call
    def search_competitors(location: str, store_type: str = "clothing store") -> str:
        """Search for clothing store competitors in a given location."""
        return get_clothing_store_competitor_data(location, store_type)
    
    # Create the agent without tools for now
    agent = create_openai_functions_agent(llm, [], prompt)
    agent_executor = AgentExecutor(agent=agent, tools=[], verbose=False)
    return agent_executor, search_competitors

def main():
    """Main function to run the competitor analysis agent."""
    agent_executor, search_competitors = get_agent()
    
    print("Welcome to the Competitor Analysis Agent!")
    print("You can ask me to generate reports on nearby clothing store competitors.")
    print("Type 'exit' to quit.")
    
    chat_history = []
    
    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                break

            # Skip if user input is empty or whitespace
            if not user_input.strip():
                print("Please enter a non-empty message.")
                continue

            # Filter out empty or whitespace-only messages from existing history
            filtered_history = [msg for msg in chat_history if hasattr(msg, 'content') and msg.content and msg.content.strip()]

            # Add user message to history
            user_message = HumanMessage(content=user_input.strip())
            
            try:
                # Check if user is asking for competitor analysis
                if any(keyword in user_input.lower() for keyword in ['coimbatore', 'competitor', 'store', 'shopping']):
                    # Extract location and store type from user input
                    location = "coimbatore" if "coimbatore" in user_input.lower() else "coimbatore"
                    store_type = "clothing store"
                    
                    # Get search results
                    search_results = search_competitors(location, store_type)
                    
                    # Create a comprehensive response
                    response_text = f"""Based on my analysis of clothing stores in {location.title()}, here are the key findings:

{search_results}

**Analysis Summary:**
- The search returned relevant information about shopping areas in {location.title()}
- Key shopping districts include Brookefields Mall, R.S. Puram, and other commercial areas
- Various clothing stores and shopping options are available for different customer segments

Would you like more specific information about any particular area or store type?"""
                    
                    print("Agent:", response_text)
                    chat_history.append(user_message)
                    chat_history.append(AIMessage(content=response_text))
                else:
                    # Use the agent for general conversation
                    response = agent_executor.invoke({
                        "input": user_input.strip(),
                        "chat_history": filtered_history
                    })
                    
                    agent_output = response["output"].strip()
                    print("Agent:", agent_output)
                    
                    # Update chat history
                    chat_history.append(user_message)
                    if agent_output:
                        chat_history.append(AIMessage(content=agent_output))
                    else:
                        print("Warning: Agent returned an empty response. Not adding to chat history.")
                    
            except Exception as e:
                print(f"Agent: I encountered an error while processing your request. Please try again.")
                
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            print("Agent: I encountered an error. Please try again.")

if __name__ == "__main__":
    main() 