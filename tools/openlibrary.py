from langchain.tools import tool
from utils.spinner import Spinner
import requests


def _parse_query_and_params(q: str):
    tokens = q.strip().split()
    params = {}
    query_tokens = []
    for t in tokens:
        if "=" in t and len(t.split("=", 1)) == 2:
            k, v = t.split("=", 1)
            params[k.strip()] = v.strip()
        else:
            query_tokens.append(t)
    clean_q = " ".join(query_tokens).strip()
    return clean_q, params


@tool
def openlibrary_search(query: str) -> str:
    """
    Search Open Library for books/works (no API key).

    Input: free-text query, with optional inline params:
      - limit=<int> (default 10)
    Example: "python programming limit=5"

    Returns: Markdown list with title, author, year, and Open Library URL.
    """
    s = Spinner("Running openlibrary_search…")
    s.start()
    try:
        clean_q, params = _parse_query_and_params(query)
        limit = int(params.get("limit", 10))

        url = "https://openlibrary.org/search.json"
        req_params = {"q": clean_q, "limit": limit}
        resp = requests.get(url, params=req_params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        docs = data.get("docs", [])

        if not docs:
            s.stop(success=True)
            return "No results from Open Library."

        lines = ["### Open Library Results"]
        for i, d in enumerate(docs, 1):
            title = (d.get("title") or "(no title)").strip()
            authors = d.get("author_name") or []
            author = ", ".join(authors[:3]) if authors else "Unknown"
            year = d.get("first_publish_year") or "n/a"
            key = d.get("key") or ""
            url_item = f"https://openlibrary.org{key}" if key else ""
            lines.append(f"{i}. {title} ({year}) — {author} — {url_item}")

        s.stop(success=True)
        return "\n".join(lines)
    except Exception as e:
        s.stop(success=False)
        return f"Open Library Error: {e}"
