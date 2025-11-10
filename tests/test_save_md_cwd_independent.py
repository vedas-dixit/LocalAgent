import os
import re
import tempfile
from pathlib import Path
from tools.save_md import save_md_locally


def test_save_md_ignores_cwd_and_writes_to_project_root(tmp_path):
    original_cwd = os.getcwd()
    try:
        os.chdir(tmp_path)
        res = save_md_locally.run("Hello from CWD test", "cwd_test.md")
        assert isinstance(res, str)
        m = re.search(r"Markdown saved successfully: (.*\.md)$", res)
        assert m, f"Unexpected response: {res}"
        saved_path = Path(m.group(1))
        assert saved_path.exists()
        assert saved_path.parent.name == "LocalStore"
        assert Path(original_cwd) in saved_path.parents
    finally:
        os.chdir(original_cwd)
        try:
            if 'saved_path' in locals() and saved_path.exists():
                saved_path.unlink()
        except Exception:
            pass
