from langchain_community.tools import DuckDuckGoSearchRun, DuckDuckGoSearchResults
from langchain.tools import tool
from utils.spinner import Spinner

@tool
def duck_duck_go_search(query: str) -> str:
    """Search DuckDuckGo for a given query."""
    s = Spinner("Running duck_duck_go_search…")
    s.start()
    try:
        search = DuckDuckGoSearchRun()
        res = search.run(query)
        s.stop(success=True)
        return res
    except Exception as e:
        s.stop(success=False)
        return f"Error: {e}"
@tool
def duck_duck_go_search_results(query: str) -> str:
    """Search DuckDuckGo for a given query and return the results."""
    s = Spinner("Running duck_duck_go_search_results…")
    s.start()
    try:
        search = DuckDuckGoSearchResults()
        res = search.run(query)
        s.stop(success=True)
        return res
    except Exception as e:
        s.stop(success=False)
        return f"Error: {e}"