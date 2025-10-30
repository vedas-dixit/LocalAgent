from langchain_community.utilities import SerpAPIWrapper
from langchain.tools import tool
from utils.spinner import Spinner
import os
from dotenv import load_dotenv

load_dotenv()

SERP_API_KEY = os.getenv("SERPAPI_API_KEY")

search = SerpAPIWrapper(serpapi_api_key=SERP_API_KEY)

@tool
def serp_search(query: str) -> str:
    """Search the web using SerpAPI (Google). Returns summarized search results."""
    s = Spinner("Running serp_search…")
    s.start()
    try:
        res = search.run(query, params={"hl": "en", "gl": "us"})
        s.stop(success=True)
        return res
    except Exception as e:
        s.stop(success=False)
        return f"Error running SerpAPI search: {e}"