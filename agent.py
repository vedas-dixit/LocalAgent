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

    result = agent.invoke(
        {"messages": [{"role": "user", "content": x}]},
        config=config
    )
    final = result["messages"][-1].content
    print("\n🤖 Agent Final Answer:\n", final)


if __name__ == "__main__":
    main()