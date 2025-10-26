from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from tools.wiki import wiki_search
from tools.math import smart_math
from tools.duckduckgo import duck_duck_go_search, duck_duck_go_search_results
from dotenv import load_dotenv
import os


def main():
    x = input("ask anything")
    load_dotenv()
    system_prompt = os.getenv("System_Prompt")

    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.7)
    config = RunnableConfig(tags=["debug", "local"],recursion_limit=100)
    agent = create_agent(
        model=llm,
        tools=[wiki_search, smart_math, duck_duck_go_search, duck_duck_go_search_results],
        system_prompt = (
            "You are an intelligent research and reasoning agent. "
            "You can think, plan, and use tools when necessary to answer questions accurately. "
            "Your available tools are:\n"
            "1. wiki_search(query: str) → Use this for factual or general knowledge queries.\n"
            "2. duck_duck_go_search(query: str) → Use this for recent or trending information.\n"
            "3. duck_duck_go_search_results(query: str) → Use when you need URLs, sources, or detailed snippets.\n"
            "4. smart_math(expression: str) → Use for calculations, equations, or numeric reasoning.\n\n"
            "Rules:\n"
            "- Always reason about which tool to use before calling it.\n"
            "- Use only one tool at a time unless combining data logically.\n"
            "- If a question asks for recent or 'latest' data, prefer DuckDuckGo tools.\n"
            "- For known facts (e.g., history, definitions, biology), prefer Wikipedia.\n"
            "- For mathematical operations, use smart_math.\n"
            "- If the user asks for explanation or context, write the answer in clear natural language.\n"
            "- Do NOT repeat tool calls for the same query.\n"
            "- After getting tool results, think briefly and give your final answer clearly.\n\n"
            "Your goal is to act like a thoughtful AI researcher — accurate, logical, and concise."
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