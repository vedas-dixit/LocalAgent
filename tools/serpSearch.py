from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import tool
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_API_KEY")

search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)

@tool
def serp_search(query: str) -> str:
    """Search the web using SerpAPI (Google). Returns summarized search results."""
    try:
        return search.run(query, params={"hl": "en", "gl": "us"})
    except Exception as e:
        return f"Error running SerpAPI search: {e}"