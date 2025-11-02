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
def europe_pmc_search(query: str) -> str:
    """
    Search Europe PMC (biomedical literature) without an API key.

    Input: free-text query, with optional inline params:
      - pageSize=<int> (default 10)
    Example: "CRISPR pageSize=5"

    Returns: Markdown list of results with title, year, journal, DOI/PMCID/PMID.
    """
    s = Spinner("Running europe_pmc_search…")
    s.start()
    try:
        clean_q, params = _parse_query_and_params(query)
        page_size = int(params.get("pageSize", 10))

        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        req_params = {"query": clean_q, "format": "json", "pageSize": page_size}
        resp = requests.get(url, params=req_params, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        results = data.get("resultList", {}).get("result", [])

        if not results:
            s.stop(success=True)
            return "No results from Europe PMC."

        lines = ["### Europe PMC Results"]
        for i, r in enumerate(results, 1):
            title = (r.get("title") or "(no title)").strip()
            year = r.get("pubYear") or "n/a"
            journal = r.get("journalTitle") or ""
            doi = r.get("doi")
            pmcid = r.get("pmcid")
            pmid = r.get("pmid")
            id_line = ", ".join(
                [p for p in [f"DOI: {doi}" if doi else None, f"PMCID: {pmcid}" if pmcid else None, f"PMID: {pmid}" if pmid else None] if p]
            )
            link = r.get("fullTextUrlList", {}).get("fullTextUrl", [])
            first_link = link[0]["url"] if link else ""
            lines.append(f"{i}. {title} ({year}) — {journal} — {id_line} {first_link}")

        s.stop(success=True)
        return "\n".join(lines)
    except Exception as e:
        s.stop(success=False)
        return f"Europe PMC Error: {e}"
