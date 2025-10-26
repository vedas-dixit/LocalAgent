from langchain.tools import tool
import wikipedia

@tool
def wiki_search(query: str) -> str:
    """Search Wikipedia and return a short summary."""
    print("wiki_search called \n",query)
    try:
        res = wikipedia.summary(query, sentences=100)
        print(res)
        return res
    except Exception as e:
        return f"Error: {e}"