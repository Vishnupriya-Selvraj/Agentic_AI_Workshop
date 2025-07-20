
import os
import bs4
from dotenv import load_dotenv

from langchain import hub
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.tools import tool
from pydantic import BaseModel # Import BaseModel

from langgraph.graph import StateGraph, END

from tavily import TavilyClient

load_dotenv()

# Configure Google API key
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# Configure Tavily API key
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def web_search(query: str):
    """Searches the web for the given query and returns the results."""
    search_results = tavily.search(query=query)
    # Extract URLs from search results
    urls = [result["url"] for result in search_results["results"]]
    if not urls:
        return "No relevant web pages found."
    
    # Load content from the URLs
    loader = WebBaseLoader(web_paths=urls)
    docs = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(splits, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
    retriever = vectorstore.as_retriever()
    
    retrieved_docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in retrieved_docs])


@tool
def rag_retrieve(query: str):
    """Retrieves information from a predefined knowledge base based on the query."""
    # Load the knowledge base from a local file
    loader = TextLoader("knowledge_base.txt")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    vectorstore = FAISS.from_documents(splits, embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"))
    retriever = vectorstore.as_retriever()
    
    retrieved_docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in retrieved_docs])


class AgentState(BaseModel):
    query: str = ""
    research_result: str = ""
    rag_result: str = ""
    final_response: str = ""
    next_step: str = ""


def router_agent(state: AgentState):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
    if "latest" in state.query.lower() or "current" in state.query.lower():
        return {"next_step": "web_research"}
    else:
        return {"next_step": "rag"} # Default to RAG if no web keywords


def web_research_agent(state: AgentState):
    print("Performing web research...")
    research_result = web_search.run(state.query)
    return {"research_result": research_result}


def rag_agent(state: AgentState):
    print("Retrieving from knowledge base...")
    rag_result = rag_retrieve.run(state.query)
    return {"rag_result": rag_result}


def summarization_agent(state: AgentState):
    print("Summarizing information...")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
    prompt = f"""Synthesize the following information into a structured response:\n\nWeb Research Result: {state.research_result}\nKnowledge Base Result: {state.rag_result}\n\nFinal Answer:"""
    final_response = llm.invoke(prompt)
    return {"final_response": final_response.content}


def call_llm(state: AgentState):
    print("Calling LLM for general query...")
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", temperature=0)
    prompt = f"""Answer the following query: {state.query}"""
    response = llm.invoke(prompt)
    return {"final_response": response.content}


# Define the LangGraph workflow
workflow = StateGraph(AgentState)

workflow.add_node("router", router_agent)
workflow.add_node("web_research", web_research_agent)
workflow.add_node("rag", rag_agent)
workflow.add_node("summarizer", summarization_agent)
workflow.add_node("llm", call_llm)

workflow.set_entry_point("router")

workflow.add_conditional_edges(
    "router",
    lambda state: state.next_step, # Use the value from the state for conditional routing
    {
        "web_research": "web_research",
        "rag": "rag",
        "llm": "llm"  
    },
)

workflow.add_edge("web_research", "summarizer")
workflow.add_edge("rag", "summarizer")
workflow.add_edge("llm", END)
workflow.add_edge("summarizer", END)

app = workflow.compile()


def run_agent(query: str):
    initial_state = AgentState(query=query)
    final_state = app.invoke(initial_state)
    return final_state.get("final_response", "No final response generated.")


if __name__ == "__main__":
    # Example Usage:
    print("\n--- Query: Latest news on AI ---")
    response = run_agent("Latest news on AI")
    print(response)

    print("\n--- Query: What is the capital of France? ---")
    response = run_agent("What is the capital of France?")
    print(response) 