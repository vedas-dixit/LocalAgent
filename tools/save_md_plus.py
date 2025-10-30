from langchain.tools import tool
from datetime import datetime
from pathlib import Path
from utils.spinner import Spinner

@tool
def save_md_plus(content: str, filename: str = None) -> str:
    """
    Append research segments to an existing Markdown file (./LocalStore).
    If the file doesn't exist, it is created automatically.
    Each call adds a timestamped section so multiple runs can build one long report.
    """
    s = Spinner("Running save_md_plus…")
    s.start()
    try:
        store_dir = Path("./LocalStore")
        store_dir.mkdir(parents=True, exist_ok=True)

        # auto-generate name
        if not filename:
            date_tag = datetime.now().strftime("%Y-%m-%d")
            filename = f"Kurama_Research_{date_tag}.md"
        if not filename.endswith(".md"):
            filename += ".md"

        file_path = store_dir / filename
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # compose section
        section = (
            f"\n\n---\n### Segment added {now}\n\n{content.strip()}\n"
        )

        # append or create
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(section)

        s.stop(success=True)
        return f"Markdown segment appended: {file_path.resolve()}"

    except Exception as e:
        s.stop(success=False)
        return f"Error appending markdown: {e}"
