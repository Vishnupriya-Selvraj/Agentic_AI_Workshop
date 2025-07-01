import os
from tavily import TavilyClient
from dotenv import load_dotenv
from typing import List, Dict, Any
import time

load_dotenv()

class TavilySearch:
    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            raise ValueError("TAVILY_API_KEY not found in environment")
        self.client = TavilyClient(api_key=api_key)
        self.rate_limit = 3  # requests per second
        self.last_request = 0
    
    async def search(self, query: str, max_results: int = 3) -> List[Dict[str, Any]]:
        """Perform rate-limited web search"""
        try:
            # Rate limiting
            elapsed = time.time() - self.last_request
            if elapsed < 1/self.rate_limit:
                time.sleep((1/self.rate_limit) - elapsed)
            
            self.last_request = time.time()
            
            response = self.client.search(
                query=query,
                search_depth="basic",
                include_answer=True,
                include_raw_content=True,
                max_results=max_results
            )
            
            return response.get("results", [])
        except Exception as e:
            print(f"Tavily search error: {str(e)}")
            return []