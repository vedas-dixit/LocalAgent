from langchain_ollama import ChatOllama
from langchain.tools import tool
from utils.spinner import Spinner

@tool
def summarize_text(text: str) -> str:
    """
    Summarizes a given text using the local Ollama LLM.
    Useful for summarizing research reports, markdowns, or long notes.
    """
    s = Spinner("Running summarize_text…")
    s.start()
    try:
        llm = ChatOllama(model="gpt-oss:120b-cloud", temperature=0.7)
        prompt = (
            "Summarize the following text in clear, structured Markdown format. "
            "Keep all essential details, and include a 'Key Takeaway' section at the end:\n\n"
            f"{text}"
        )
        summary = llm.invoke(prompt)
        s.stop(success=True)
        return summary.content if hasattr(summary, "content") else summary
    except Exception as e:
        s.stop(success=False)
        return f"Summarization error: {str(e)}"
    