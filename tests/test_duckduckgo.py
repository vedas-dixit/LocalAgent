from tools.duckduckgo import duck_duck_go_search, duck_duck_go_search_results

def test_duckduckgo_search():
    res = duck_duck_go_search.run("quantum computing 2025")
    assert isinstance(res, str)
    assert len(res) > 0

def test_duckduckgo_search_results():
    res = duck_duck_go_search_results.run("latest AI models 2025")
    assert isinstance(res, str)
