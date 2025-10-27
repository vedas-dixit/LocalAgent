from tools.wiki import wiki_search

def test_wiki_search_basic():
    """Ensure wiki_search runs and returns text or a clear error."""
    res = wiki_search.run("Transformer (machine learning)")
    assert isinstance(res, str)
    assert len(res) > 0
