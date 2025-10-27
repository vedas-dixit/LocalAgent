from tools.arxiv_tool import arxiv_search

def test_arxiv_search():
    res = arxiv_search.run("attention is all you need")
    assert isinstance(res, str)
    assert "Published:" in res or "Title:" in res
