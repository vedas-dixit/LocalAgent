from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langchain_core.runnables import RunnableConfig
from tools.tools_wrapper import tools
from prompts.research_prompt import KURAMA_RESEARCH_PROMPT_GENERIC, KURAMA_RESEARCH_PROMPT_DEEPRESEARCH,KURAMA_RESEARCH_PROMPT
from dotenv import load_dotenv
from utils.spinner import Spinner
from utils.markdown_render import render_markdown
from langgraph.errors import GraphRecursionError
from pyfiglet import Figlet

def main():

    load_dotenv()
    f = Figlet(font='standard')
    print(f.renderText('Kurama v 1.3'))
    x = input("Ask Kurama 🦊\n")

    llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.7,verbose=True)
    recursion_limit = 50
    config = RunnableConfig(tags=["debug", "local"], recursion_limit=recursion_limit)
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=KURAMA_RESEARCH_PROMPT
    )

    result = None
    MAX_RECURSION_LIMIT = 100
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