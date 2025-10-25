from langchain.tools import tool
import math

@tool
def smart_math(expression: str) -> float:
    """Safely evaluate a mathematical expression (supports +, -, *, /, **, sqrt, sin, etc.)."""
    try:
        allowed = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
        result = eval(expression, {"__builtins__": {}}, allowed)
        return result
    except Exception as e:
        return f"Error evaluating expression: {e}"
