import os
from dotenv import load_dotenv
from posthog import api_key
from langchain_community.tools.asknews import AskNewsSearch
from langchain.tools import tool

load_dotenv()
ASKNEWS_CLIENT_ID = os.getenv("ASKNEWS_CLIENT_ID")
ASKNEWS_CLIENT_SECRET = os.getenv("ASKNEWS_CLIENT_SECRET")

if not ASKNEWS_CLIENT_ID or not ASKNEWS_CLIENT_SECRET:
    raise ValueError("Please set the ASKNEWS_CLIENT_ID and ASKNEWS_CLIENT_SECRET environment variables.")

@tool
def asknews_search(query: str) -> str:
    """
    Search the latest news using AskNews (free-tier).
    Returns summarized news results with titles and short snippets.
    Ideal for queries like 'latest AI research', 'SpaceX news', or 'tech layoffs 2025'.
    """
    try:
        search = AskNewsSearch(client_id=ASKNEWS_CLIENT_ID, client_secret=ASKNEWS_CLIENT_SECRET)
        results = search.run(query)
        return results
    except Exception as e:
        return f"AskNews Error: {e}"