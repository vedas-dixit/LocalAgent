from langchain_community.utilities import ArxivAPIWrapper
from langchain.tools import tool
from utils.spinner import Spinner

# Initialize the wrapper once
arxiv = ArxivAPIWrapper()

@tool
def arxiv_search(query: str) -> str:
    """
    Search research papers from arXiv.
    Returns publishing date, title, authors, and summary.
    Use this for scientific, academic, or AI research-related questions.
    """
    s = Spinner("Running arxiv_search…")
    s.start()
    try:
        results = arxiv.run(query)
        s.stop(success=True)
        return results
    except Exception as e:
        s.stop(success=False)
        return f"Arxiv Error: {e}"
