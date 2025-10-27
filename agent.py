from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from tools.wiki import wiki_search
from tools.math import smart_math
from tools.getNews import asknews_search
from tools.arxiv_tool import arxiv_search
from tools.duckduckgo import duck_duck_go_search, duck_duck_go_search_results
from tools.getDate import get_current_date
from retriever import add_to_db,query_db
from prompts.research_prompt import KURAMA_RESEARCH_PROMPT
from dotenv import load_dotenv
import os
from utils.spinner import Spinner
from utils.markdown_render import render_markdown


def main():
    x = input("Ask Kurama 🦊\n")
    load_dotenv()

    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.7)
    config = RunnableConfig(tags=["debug", "local"],recursion_limit=100)
    agent = create_agent(
        model=llm,
        tools=[wiki_search, smart_math, duck_duck_go_search, duck_duck_go_search_results, add_to_db, query_db, asknews_search, arxiv_search,get_current_date],
        system_prompt=KURAMA_RESEARCH_PROMPT
    )

    # Show a live spinner while the agent reasons and calls tools
    s = Spinner("Reasoning | Choosing tools | Gathering info")
    s.start()
    try:
        result = agent.invoke(
            {"messages": [{"role": "user", "content": x}]},
            config=config
        )
        s.stop(success=True)
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