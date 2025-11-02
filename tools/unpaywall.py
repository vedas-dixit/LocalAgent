from langchain.tools import tool
from utils.spinner import Spinner
import os
import requests


def _headers() -> dict:
    email = os.getenv("UNPAYWALL_EMAIL") or os.getenv("CONTACT_EMAIL")
    ua = (
        f"LocalAgent/1.0 (+mailto:{email})"
        if email
        else "LocalAgent/1.0 (https://github.com/vedas-dixit/LocalAgent)"
    )
    return {
        "User-Agent": ua,
        "Accept": "application/json",
    }


def _parse_input(s: str):
    """
    Expect: "<doi> [email=user@example.com]"
    Returns (doi, email or None)
    """
    parts = s.strip().split()
    doi = parts[0] if parts else ""
    email = None
    for p in parts[1:]:
        if p.startswith("email="):
            email = p.split("=", 1)[1].strip()
    return doi, email


@tool
def unpaywall_lookup(doi_and_email: str) -> str:
    """
    Look up Open-Access availability for a DOI using Unpaywall (no API key).

    Input format: "<doi> [email=user@example.com]"
    - You must provide an email either inline or via env var UNPAYWALL_EMAIL.

    Returns: OA locations, best OA URL, and license info if available.
    """
    s = Spinner("Running unpaywall_lookup…")
    s.start()
    try:
        doi, email_inline = _parse_input(doi_and_email)
        email = email_inline or os.getenv("UNPAYWALL_EMAIL") or os.getenv("CONTACT_EMAIL")
        if not doi:
            s.stop(success=False)
            return "Error: Provide a DOI, e.g. '10.1038/nature12373 email=you@example.com'"
        if not email:
            s.stop(success=False)
            return (
                "Error: Unpaywall requires an email. Provide as 'email=you@example.com' "
                "or set UNPAYWALL_EMAIL in your environment."
            )

        url = f"https://api.unpaywall.org/v2/{doi}"
        params = {"email": email}
        resp = requests.get(url, params=params, headers=_headers(), timeout=20)
        if resp.status_code == 404:
            s.stop(success=True)
            return "No Unpaywall record found for this DOI."
        resp.raise_for_status()
        data = resp.json()

        best = data.get("best_oa_location") or {}
        best_url = best.get("url") or best.get("url_for_pdf") or best.get("url_for_landing_page")
        license_ = best.get("license") or data.get("license")
        is_oa = data.get("is_oa")

        lines = [
            f"### Unpaywall for DOI {doi}",
            f"- is_oa: {is_oa}",
            f"- best_oa_url: {best_url if best_url else 'n/a'}",
            f"- license: {license_ if license_ else 'n/a'}",
        ]

        # Include a few OA locations if present
        locs = data.get("oa_locations") or []
        if locs:
            lines.append("- oa_locations:")
            for i, loc in enumerate(locs[:5], 1):
                u = loc.get("url") or loc.get("url_for_pdf") or loc.get("url_for_landing_page")
                host = loc.get("host_type")
                ver = loc.get("version")
                lines.append(f"  {i}. {u} (host={host}, version={ver})")

        s.stop(success=True)
        return "\n".join(lines)
    except Exception as e:
        s.stop(success=False)
        return f"Unpaywall Error: {e}"
