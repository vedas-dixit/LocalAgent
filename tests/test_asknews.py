import os
from tools.getNews import asknews_search

def test_asknews_search_env():
    assert os.getenv("ASKNEWS_CLIENT_ID"), "Missing AskNews Client ID"
    assert os.getenv("ASKNEWS_CLIENT_SECRET"), "Missing AskNews Secret"

def test_asknews_search_run():
    res = asknews_search.run("AI breakthroughs 2025")
    assert isinstance(res, str)
