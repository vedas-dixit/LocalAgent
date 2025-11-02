from langchain.tools import tool
from utils.spinner import Spinner
import os
import requests


def _headers() -> dict:
    email = os.getenv("CONTACT_EMAIL") or os.getenv("UNPAYWALL_EMAIL")
    ua = (
        f"LocalAgent/1.0 (+mailto:{email})"
        if email
        else "LocalAgent/1.0 (https://github.com/vedas-dixit/LocalAgent)"
    )
    return {
        "User-Agent": ua,
        "Accept": "application/json",
    }


def _parse_query_and_params(q: str):
    """
    Allow simple inline params e.g.:
      "neural networks rows=20 sort=relevance order=desc"
    Returns (clean_query, params_dict)
    """
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
def crossref_search(query: str) -> str:
    """
    Search Crossref for works (papers, DOIs) without an API key.

    Input: free-text query, with optional inline params:
      - rows=<int> (default 10)
      - sort=<relevance|published|created>
      - order=<asc|desc>
    Example: "neural network rows=20 sort=relevance"

    Returns: Markdown list of top results with title, year, DOI, URL.
    """
    s = Spinner("Running crossref_search…")
    s.start()
    try:
        clean_q, params = _parse_query_and_params(query)
        rows = int(params.get("rows", 10))
        sort = params.get("sort")
        order = params.get("order")

        url = "https://api.crossref.org/works"
        req_params = {"query": clean_q, "rows": rows}
        if sort:
            req_params["sort"] = sort
        if order:
            req_params["order"] = order

        resp = requests.get(url, params=req_params, headers=_headers(), timeout=20)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("message", {}).get("items", [])

        if not items:
            s.stop(success=True)
            return "No results from Crossref."

        lines = ["### Crossref Results"]
        for i, it in enumerate(items, 1):
            title = "; ".join(it.get("title", [])).strip() or "(no title)"
            doi = it.get("DOI", "")
            year = None
            y = it.get("issued", {}).get("date-parts")
            if isinstance(y, list) and y and isinstance(y[0], list) and y[0]:
                year = y[0][0]
            url_item = (it.get("URL") or (f"https://doi.org/{doi}" if doi else "")).strip()
            lines.append(f"{i}. {title} ({year if year else 'n/a'}) — DOI: {doi} — {url_item}")

        s.stop(success=True)
        return "\n".join(lines)
    except Exception as e:
        s.stop(success=False)
        return f"Crossref Error: {e}"
