from tools.wiki import wiki_search
from tools.math import smart_math
from tools.getNews import asknews_search
from tools.arxiv_tool import arxiv_search
from tools.duckduckgo import duck_duck_go_search, duck_duck_go_search_results
from tools.getDate import get_current_date
from tools.save_md import save_md_locally
from tools.summarize_text import summarize_text
from tools.serpSearch import serp_search
from tools.save_md_plus import save_md_plus
from tools.SearxNG import searx_search
from tools.crossref import crossref_search
from tools.unpaywall import unpaywall_lookup
from tools.europe_pmc import europe_pmc_search
from tools.openlibrary import openlibrary_search
from retriever import add_to_db,query_db


tools=[ 
    wiki_search,
            smart_math,
            duck_duck_go_search,
            duck_duck_go_search_results,
            searx_search,
            add_to_db,
            query_db,
            asknews_search,
            serp_search,
            arxiv_search,
            crossref_search,
            unpaywall_lookup,
            europe_pmc_search,
            openlibrary_search,
            get_current_date,
            save_md_locally,
            save_md_plus,
            summarize_text
        ]