import os
from datetime import datetime
from langchain.tools import tool
HISTORY_FILE = os.path.join(os.path.dirname(__file__), "history.txt")

@tool
def read_history(query: str = None) -> str:
    """Read history file. 
    If query provided, return related lines; otherwise full history summary."""
    print("read_history called")
    if not os.path.exists(HISTORY_FILE):
        return ""

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Clean
    lines = [l.strip() for l in lines if l.strip()]

    # Optional filter: return only matching lines
    if query:
        related = [l for l in lines if query.lower() in l.lower()]
        return "\n".join(related[-5:]) if related else ""
    return "\n".join(lines[-10:])  # show last 10 entries

@tool
def write_history(prompt: str, response: str) -> None:
    """Write or update user–agent interactions, avoiding excessive growth."""
    # Create file if missing
    print("write_history called")
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    # Append new entry
    with open(HISTORY_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n")
        f.write(f"User: {prompt.strip()}\n")
        f.write(f"Agent: {response.strip()}\n\n")

    # Prune if file grows too large (avoid infinite growth)
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if len(lines) > 1000:  # limit to ~500 messages
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines[-800:])
