from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
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
from prompts.research_prompt import KURAMA_RESEARCH_PROMPT_GENERIC, KURAMA_RESEARCH_PROMPT_DEEPRESEARCH
from dotenv import load_dotenv
import os
from utils.spinner import Spinner
from utils.markdown_render import render_markdown
from utils.llm_config import get_chat_model
from langgraph.errors import GraphRecursionError


def main():
    x = input("Ask Kurama 🦊\n")
    load_dotenv()

    # Get chat model based on configured provider
    llm = get_chat_model()
    recursion_limit = 100
    config = RunnableConfig(tags=["debug", "local"], recursion_limit=recursion_limit)
    agent = create_agent(
        model=llm,
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
            summarize_text,
        ],
        system_prompt=KURAMA_RESEARCH_PROMPT_GENERIC
    )

    result = None
    MAX_RECURSION_LIMIT = 1000
    while True:
        s = Spinner("Reasoning | Choosing tools | Gathering info")
        s.start()
        try:
            config = RunnableConfig(tags=["debug", "local"], recursion_limit=recursion_limit)
            result = agent.invoke(
                {"messages": [{"role": "user", "content": x}]},
                config=config
            )
            s.stop(success=True)
            break
        except GraphRecursionError:
            s.stop(success=False)
            print(f"\nRecursion limit of {recursion_limit} reached.")
            choice = input("Continue research with more steps? [y/N]: ").strip().lower()
            if choice != "y":
                print("Stopped by user.")
                return
            increment = 50
            recursion_limit = min(recursion_limit + increment, MAX_RECURSION_LIMIT)
            if recursion_limit >= MAX_RECURSION_LIMIT:
                print(f"Reached max allowed recursion limit ({MAX_RECURSION_LIMIT}). Aborting.")
                return
            # loop and try again with higher limit
        except Exception:
            s.stop(success=False)
            raise

    final = result["messages"][-1].content

    # Render the final markdown nicely in the terminal
    rs = Spinner("Rendering markdown…")
    rs.start()
    try:
        render_markdown(final, title="🦊 Kurama Research Report")
        rs.stop(success=True)
    except Exception:
        rs.stop(success=False)
        # Fallback to plain print
        print("\n🦊 Kurama | Answer:\n")
        print(final)



if __name__ == "__main__":
    main()