import os
from tools.serpSearch import serp_search


def test_serp_search_returns_string():
    res = serp_search.run("transformer attention site:arxiv.org")
    assert isinstance(res, str)
    assert len(res) > 0
    if not os.getenv("SERPAPI_API_KEY"):
        assert "error" in res.lower()
