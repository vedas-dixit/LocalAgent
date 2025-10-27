from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain.tools import tool

@tool
def duck_duck_go_search(query: str) -> str:
    """Search DuckDuckGo for a given query."""
    search = DuckDuckGoSearchRun()
    res = search.run(query)
    return res
@tool
def duck_duck_go_search_results(query: str) -> str:
    """Search DuckDuckGo for a given query and return the results."""
    search = DuckDuckGoSearchResults()
    res = search.run(query)
    return res