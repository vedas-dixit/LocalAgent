from langchain.tools import tool

@tool
def multiply_by(num1: float,num2: float) -> float:
    """Multiply two number"""
    return num1 * num2