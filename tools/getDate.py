from datetime import datetime
from langchain.tools import tool
from utils.spinner import Spinner

@tool
def get_current_date():
    """Returns the current date as a string in YYYY-MM-DD format."""
    s = Spinner("Running get_current_date…")
    s.start()
    try:
        res = datetime.now().strftime("%Y-%m-%d")
        s.stop(success=True)
        return res
    except Exception:
        s.stop(success=False)
        raise