from langchain_community.utilities import SearxSearchWrapper
from langchain_community.tools import SearxSearchResults
from langchain.tools import tool
from utils.spinner import Spinner
import os
from dotenv import load_dotenv

load_dotenv()
wrapper = SearxSearchWrapper(
    searx_host=os.getenv("SEARX_INSTANCE_URL"),
    k=int(os.getenv("SEARX_TOP_K_RESULTS", 5)),
)

searx_tool = SearxSearchResults(
    searx_instance_url=os.getenv("SEARX_INSTANCE_URL"),
    top_k_results=int(os.getenv("SEARX_TOP_K_RESULTS", 5)),
    wrapper=wrapper
)

@tool
def searx_search(query: str) -> str:
    """
    Search the web using a SearxNG instance.
    Returns summarized search results with titles and short snippets.
    Ideal for general web searches and information retrieval.
    """
    s = Spinner("Running searx_search…")
    s.start()
    try:
        res = searx_tool.run(query)
        s.stop(success=True)
        return res
    except Exception as e:
        s.stop(success=False)
        return f"Error: {e}"


