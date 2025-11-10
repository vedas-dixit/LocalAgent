import os
from langchain.tools import tool
from datetime import datetime
from pathlib import Path
from utils.spinner import Spinner


def _detect_project_root() -> Path:
    """Best-effort detection of the project root directory.

    Priority:
    1) Parent folders of this file that contain common repo markers (README.md + tools/)
    2) Current working directory if it looks like the repo
    3) Fallback to current working directory
    """
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

    # Try CWD if it looks like the repo
    cwd = Path.cwd()
    if any((cwd / m).exists() for m in markers) and (cwd / "tools").exists():
        return cwd

    return cwd

@tool
def save_md_locally(content: str, filename: str = None) -> str:
    """
    Save the given markdown content into a structured local directory (./LocalStore).
    If no filename is provided, generates one automatically with a timestamp.
    """
    s = Spinner("Running save_md_locally…")
    s.start()
    try:
        # Allow override via env var for fully explicit control
        override_dir = os.getenv("LOCALAGENT_OUTPUT_DIR")
        if override_dir:
            store_dir = Path(override_dir).expanduser().resolve()
        else:
            # Default to project root/LocalStore, not process CWD
            project_root = _detect_project_root()
            store_dir = (project_root / "LocalStore").resolve()

        store_dir.mkdir(parents=True, exist_ok=True)

        if not filename:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"Kurama_Research_{timestamp}.md"

        if not filename.endswith(".md"):
            filename += ".md"

        file_path = store_dir / filename

        tmp_path = file_path.with_suffix(file_path.suffix + ".tmp")
        with open(tmp_path, "w", encoding="utf-8") as f:
            f.write(content.strip() + "\n")
        tmp_path.replace(file_path)

        s.stop(success=True)
        return f"Markdown saved successfully: {file_path.resolve()}"

    except Exception as e:
        s.stop(success=False)
        return f"Error saving markdown content: {str(e)}"
