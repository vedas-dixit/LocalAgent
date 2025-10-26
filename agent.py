from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from tools.wiki import wiki_search
from tools.math import smart_math
from tools.duckduckgo import duck_duck_go_search, duck_duck_go_search_results
from store.history import read_history,write_history
from dotenv import load_dotenv
import os


def main():
    x = input("ask anything\n")
    load_dotenv()

    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.7)
    config = RunnableConfig(tags=["debug", "local"],recursion_limit=100)
    agent = create_agent(
        model=llm,
        tools=[wiki_search, smart_math, duck_duck_go_search, duck_duck_go_search_results, read_history, write_history],
        system_prompt = (
            "You are an intelligent research and reasoning agent. "
            "You can think, plan, and use tools when necessary to answer accurately.\n\n"
            "Available tools:\n"
            "• wiki_search(query) – factual or general knowledge.\n"
            "• duck_duck_go_search(query) – recent or trending info.\n"
            "• duck_duck_go_search_results(query) – URLs and detailed snippets.\n"
            "• smart_math(expression) – numeric or mathematical reasoning.\n"
            "• read_history(query) – recall useful past user interactions.\n"
            "• write_history(entry) – save new, important insights for later.\n\n"
            "Guidelines:\n"
            "- Always reason briefly before using a tool.\n"
            "- Always check your memory with read_history if prior context might help.\n"
            "- Store reusable/generic/personal information with write_history.\n"
            "- Prefer one tool at a time unless combining results logically.\n"
            "- Use DuckDuckGo tools for 'latest' or 'recent' topics; Wikipedia for timeless facts; smart_math for calculations.\n"
            "- After gathering data, summarize clearly and avoid repeating tool calls and always store the data briefly in the memory(write_history).\n\n"
            "Your goal: act like a thoughtful AI researcher — concise, logical, and context-aware."
        )
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": x}]},
        config=config
    )
    final = result["messages"][-1].content
    print("\n🤖 Agent Final Answer:\n", final)


if __name__ == "__main__":
    main()