from langchain_ollama import ChatOllama
from langchain.tools import tool
from utils.spinner import Spinner
import os
from dotenv import load_dotenv

load_dotenv()

@tool
def summarize_text(text: str) -> str:
    """
    Summarizes a given text using Ollama LLM (local or remote API).
    Useful for summarizing research reports, markdowns, or long notes.
    """
    s = Spinner("Running summarize_text…")
    s.start()
    try:
        # Configure Ollama from environment variables
        ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        ollama_model = os.getenv("OLLAMA_CHAT_MODEL", "gpt-oss:120b-cloud")
        ollama_temperature = float(os.getenv("OLLAMA_TEMPERATURE", "0.7"))

        llm = ChatOllama(
            model=ollama_model,
            temperature=ollama_temperature,
            base_url=ollama_base_url
        )
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
    