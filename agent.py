from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
import wikipedia

@tool
def wiki_search(query: str) -> str:
    """Search Wikipedia and return a short summary."""
    try:
        res = wikipedia.summary(query, sentences=100)
        print(res)
        return res
    except Exception as e:
        return f"Error: {e}"

@tool
def multiply_by(num1: float,num2: float) -> float:
    """Multiply a number"""
    print("multiply_by called")
    return num1 * num2

def main():
    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.7)
    config = RunnableConfig(tags=["debug", "local"],recursion_limit=100)
    x = input(str("how can this agent help, it has tools like wiki_pedia or multiply by"))
    agent = create_agent(
        model=llm,
        tools=[wiki_search, multiply_by],
        system_prompt=(
            "- You are an agent.\n"
            "- you will answer the question and can use provided tools.\n"
            "- Use tool wiki_search to get factual information from wikipedia.\n"
            "- Use multiply_by only for numerical multiplication.\n"
            "- Do NOT call tools repeatedly or loop.\n"
            "- When you have answered the question, stop and respond to the user directly."
        ),
    )

    result = agent.invoke(
        {"messages": [{"role": "user", "content": x}]},
        config=config
    )
    final = result["messages"][-1].content
    print("\n🤖 Agent Final Answer:\n", final)


if __name__ == "__main__":
    main()