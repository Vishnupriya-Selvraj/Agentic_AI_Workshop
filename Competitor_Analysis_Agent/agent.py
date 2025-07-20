from langchain_core.tools import tool
from langchain_community.tools import TavilySearchResults

@tool
def get_clothing_store_competitor_data(location: str, store_type: str = "clothing store") -> str:
    """
    Searches for clothing store competitors in a given location and retrieves relevant data.
    This includes information about store footfall, busiest times, and general competitor overview.
    """
    tavily = TavilySearchResults(k=5)
    query = f"clothing store competitors in {location} footfall and busiest times"
    results = tavily.invoke({"query": query})

    # Format the results into a readable string, filtering out empty content
    formatted_results = []
    for r in results:
        content = r.get('content', '').strip() # Get content and strip whitespace
        if content: # Only add if content is not empty
            formatted_results.append(f"Title: {r['title']}\nURL: {r['url']}\nContent: {content}\n---")
    
    # If no results or all results had empty content, return a default message
    if not formatted_results:
        return "No relevant clothing store competitor data with useful content found for the given location and store type."
    
    return "\n".join(formatted_results)


def get_tools():
    return [get_clothing_store_competitor_data] 