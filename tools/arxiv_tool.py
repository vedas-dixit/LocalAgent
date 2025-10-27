from langchain_community.utilities import ArxivAPIWrapper
from langchain.tools import tool

# Initialize the wrapper once
arxiv = ArxivAPIWrapper()

@tool
def arxiv_search(query: str) -> str:
    """
    Search research papers from arXiv.
    Returns publishing date, title, authors, and summary.
    Use this for scientific, academic, or AI research-related questions.
    """
    try:
        results = arxiv.run(query)
        print(f"[Arxiv] Search successful for: {query}")
        return results
    except Exception as e:
        return f"Arxiv Error: {e}"
