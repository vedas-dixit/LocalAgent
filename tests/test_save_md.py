import os
import uuid
from tools.save_md import save_md_locally


def test_save_md_locally_creates_file_and_content():
    filename = f"test_md_{uuid.uuid4().hex}.md"
    content = "# Test Title\n\nHello from test."

    res = save_md_locally.run(content, filename)
    assert isinstance(res, str)
    assert "Markdown saved successfully" in res

    path = os.path.join("LocalStore", filename)
    try:
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        assert content.strip() in data
    finally:
        if os.path.exists(path):
            os.remove(path)
