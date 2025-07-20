from langchain_core.messages import BaseMessage, HumanMessage, AIMessage # Added AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI # Changed from langchain_openai
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_functions_agent
from agent import get_tools  # Import the get_tools function
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up environment variables
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY") # Ensure Google API key is set
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY") # Ensure Tavily API key is set

def get_agent():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0) # Changed model to Gemini

    # Tools for the agent
    tools = get_tools()

    # Prompt template for the agent
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are a helpful AI assistant. Provide detailed reports on clothing store competitors."),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )

    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor

def main():
    agent_executor = get_agent()
    chat_history = []

    print("Welcome to the Competitor Analysis Agent!")
    print("You can ask me to generate reports on nearby clothing store competitors.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break

        # Filter out empty or whitespace-only messages from existing history
        filtered_history = [msg for msg in chat_history if getattr(msg, 'content', '').strip()]

        response = agent_executor.invoke({"input": user_input, "chat_history": filtered_history})
        agent_output = response["output"].strip() # Get agent's output and strip whitespace

        print("Agent:", agent_output)
        chat_history.append(HumanMessage(content=user_input))

        # Only append AIMessage if the content is not empty
        if agent_output:
            chat_history.append(AIMessage(content=agent_output))
        else:
            print("Warning: Agent returned an empty response. Not adding to chat history.")

if __name__ == "__main__":
    main() 