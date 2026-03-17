import os
from langchain.tools import tool
from datetime import datetime
from pathlib import Path
from utils.spinner import Spinner


def _detect_project_root() -> Path:
    here = Path(__file__).resolve()
    markers = ["README.md", "requirements.txt"]
    needs_dirs = ["tools"]

    for p in [here.parent] + list(here.parents):
        try:
            if any((p / m).exists() for m in markers) and all((p / d).exists() for d in needs_dirs):
                return p
            if (p / ".git").exists() and (p / "tools").exists():
                return p
        except Exception:
            pass

    cwd = Path.cwd()
    if any((cwd / m).exists() for m in markers) and (cwd / "tools").exists():
        return cwd
    return cwd

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
        override_dir = os.getenv("LOCALAGENT_OUTPUT_DIR")
        if override_dir:
            store_dir = Path(override_dir).expanduser().resolve()
        else:
            project_root = _detect_project_root()
            store_dir = (project_root / "LocalStore").resolve()

        store_dir.mkdir(parents=True, exist_ok=True)

        if not filename:
            date_tag = datetime.now().strftime("%Y-%m-%d")
            filename = f"Kurama_Research_{date_tag}.md"
        if not filename.endswith(".md"):
            filename += ".md"

        file_path = store_dir / filename
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        section = (
            f"\n\n---\n### Segment added {now}\n\n{content.strip()}\n"
        )

        with open(file_path, "a", encoding="utf-8") as f:
            f.write(section)

        s.stop(success=True)
        return f"Markdown segment appended: {file_path.resolve()}"

    except Exception as e:
        s.stop(success=False)
        return f"Error appending markdown: {e}"
