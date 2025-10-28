from langchain.tools import tool
from datetime import datetime
from pathlib import Path
from utils.spinner import Spinner

@tool
def save_md_locally(content: str, filename: str = None) -> str:
    """
    Save the given markdown content into a structured local directory (./LocalStore).
    If no filename is provided, generates one automatically with a timestamp.
    """
    s = Spinner("Running save_md_locally…")
    s.start()
    try:
        store_dir = Path("./LocalStore")
        store_dir.mkdir(parents=True, exist_ok=True)

        if not filename:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Kurama_Research_{timestamp}.md"

        if not filename.endswith(".md"):
            filename += ".md"

        file_path = store_dir / filename

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")

        s.stop(success=True)
        return f"Markdown saved successfully: {file_path.resolve()}"

    except Exception as e:
        s.stop(success=False)
        return f"Error saving markdown content: {str(e)}"
