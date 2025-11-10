import os
import uuid
from tools.save_md_plus import save_md_plus


def test_save_md_plus_appends_segments():
    base_name = f"test_append_{uuid.uuid4().hex}"
    # Intentionally omit .md to test auto-append behavior
    res1 = save_md_plus.run({"content": "First segment", "filename": base_name})
    res2 = save_md_plus.run({"content": "Second segment", "filename": base_name})

    filename = base_name + ".md"
    path = os.path.join("LocalStore", filename)
    try:
        assert isinstance(res1, str) and isinstance(res2, str)
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        assert "First segment" in data
        assert "Second segment" in data
        assert data.count("Segment added") >= 2
    finally:
        if os.path.exists(path):
            os.remove(path)
