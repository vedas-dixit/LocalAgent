from datetime import datetime
from langchain.tools import tool

@tool
def get_current_date():
    """Returns the current date as a string in YYYY-MM-DD format."""
    return datetime.now().strftime("%Y-%m-%d")