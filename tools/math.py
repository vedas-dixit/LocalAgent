from langchain.tools import tool
import math
from utils.spinner import Spinner

@tool
def smart_math(expression: str) -> float:
    """Safely evaluate a mathematical expression (supports +, -, *, /, **, sqrt, sin, etc.)."""
    s = Spinner("Running smart_math…")
    s.start()
    try:
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        s.stop(success=True)
        return result
    except Exception as e:
        s.stop(success=False)
        return f"Error evaluating expression: {e}"
