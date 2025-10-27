from langchain.tools import tool
import wikipedia
from utils.spinner import Spinner

@tool
def wiki_search(query: str) -> str:
    """Search Wikipedia and return a short summary."""
    s = Spinner("Running wiki_search…")
    s.start()
    try:
        res = wikipedia.summary(query, sentences=100)
        s.stop(success=True)
        return res
    except Exception as e:
        s.stop(success=False)
        return f"Error: {e}"