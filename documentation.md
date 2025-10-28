# LocalAgent Documentation

This document explains what the project does, how it is structured, how to set it up on a new machine, how it runs, and how to customize it. The language here is intentionally simple and direct.

## 1. What this project is

LocalAgent is a small research assistant that runs on your computer. It uses an Ollama local language model with LangChain tools to:
- search Wikipedia and the web
- look up arXiv papers
- do simple math
- store and retrieve notes in a local vector database (ChromaDB)
- optionally read recent news using AskNews

The agent produces a Markdown answer. The terminal renders this Markdown so it is easy to read.

## 2. How it works (high level)

1. `agent.py` loads environment variables, builds an Ollama chat model, and wires a set of tools.
2. When you type a question, the agent decides which tools to call and in what order.
3. The tools return data. The agent composes a final Markdown answer.
4. The final Markdown is rendered in the terminal with an orange border using the Rich library. If Rich is not available, it prints plain text.
5. Throughout execution, a small spinner shows progress in the terminal for the agent and each tool.

## 3. Code structure

- `agent.py` — program entry point. Creates the LangChain agent, configures tools, shows a spinner during reasoning, and renders the final Markdown.
- `prompts/research_prompt.py` — the system prompt that describes how the agent should work.
- `tools/` — individual tools the agent can call:
  - `wiki.py` — Wikipedia summary
  - `duckduckgo.py` — DuckDuckGo search and search results
  - `arxiv_tool.py` — arXiv paper lookup
  - `math.py` — simple math evaluation
  - `getDate.py` — get the current date
  - `getNews.py` — AskNews search (requires API credentials)
  - `save_md.py` — save Markdown output locally as files
  - `summarize_text.py` — summarize long text using the local model
- `retriever.py` — functions to store and retrieve text from a local ChromaDB using Ollama embeddings.
- `store/chromadb.py` — sets up a persistent ChromaDB collection in `./chromadb_store`.
- `utils/spinner.py` — prints a small spinner line while a task runs, then a success or failure mark with duration.
- `utils/markdown_render.py` — renders Markdown in the terminal using Rich with an orange border. Falls back to plain printing when Rich is not installed.
- `tests/` — small tests for math, wiki, duckduckgo, arxiv, and AskNews.

## 4. Requirements

- macOS or Linux. Windows works with WSL.
- Python 3.10 or newer.
- Ollama installed and running (for the chat model and embeddings).
- Internet connection for web tools (Wikipedia, DuckDuckGo, arXiv, AskNews).

Python dependencies are listed in `requirements.txt`. A new dependency used for terminal rendering is `rich`.

## 5. Install

Create a virtual environment and install Python dependencies.

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Install Ollama and start it. On macOS with Homebrew:

```zsh
brew install ollama
ollama serve
```

You can also download the app from https://ollama.com.

## 6. Models to pull with Ollama

This project expects two models:

- Chat model used in `agent.py`:

```zsh
ollama pull gpt-oss:120b-cloud
```

- Embedding model used for memory in `retriever.py`:

```zsh
ollama pull nomic-embed-text
```

If `gpt-oss:120b-cloud` is not available on your system, change the model in `agent.py` to another model you already have locally, for example `llama3:8b` or `qwen2:7b`:

```python
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3:8b", temperature=0.7)
```

## 7. Configuration

AskNews is optional but is imported by default. To avoid startup errors, set the following environment variables in a `.env` file at the project root:

```env
ASKNEWS_CLIENT_ID=your_client_id
ASKNEWS_CLIENT_SECRET=your_client_secret
```

If you do not plan to use AskNews, remove the import and tool from `agent.py`:
- Remove `from tools.getNews import asknews_search`.
- Remove `asknews_search` from the `tools=[...]` list passed to `create_agent`.

## 8. Run

Start the agent:

```zsh
python agent.py
```

Type a question when prompted. The terminal will show live status lines while each tool runs. When the answer is ready, it will render as Markdown inside a panel. If Rich is not installed, the Markdown will be printed as plain text.

## 9. How the output is rendered

The final answer is Markdown. `utils/markdown_render.py` uses the Rich library to:
- parse and format Markdown
- draw an orange border panel
- apply a simple theme for headings, links, and code blocks

If Rich is not available, the code prints the raw Markdown string. You can install Rich by ensuring it is included in `requirements.txt` and running `pip install -r requirements.txt`.

## 10. What gets saved

- ChromaDB data is stored in `./chromadb_store`. This folder is created automatically.
- To reset local memory, delete the `chromadb_store` folder.
- Markdown reports saved by the agent (using `save_md_locally`) are stored under `./LocalStore`. This folder is created automatically. Filenames end with `.md` and default to a timestamped pattern when not provided.

## 11. Tests

There are a few small tests under `tests/`.

```zsh
pip install -U pytest
pytest -k "not asknews"   # skip AskNews tests if you did not set the .env
```

Some tests reach external services and may take time or fail without an internet connection.

## 12. Troubleshooting

- Model not found
  - Make sure you pulled the models with Ollama: `gpt-oss:120b-cloud` and `nomic-embed-text`.
  - If the chat model is not available on your system, change the model name in `agent.py` to one you have locally, such as `llama3:8b`.
- AskNews errors
  - Set `ASKNEWS_CLIENT_ID` and `ASKNEWS_CLIENT_SECRET` in `.env`, or remove the AskNews tool from the agent.
- Ollama not running
  - Start it with `ollama serve` or launch the Ollama app.
- ChromaDB issues
  - Delete the `chromadb_store` folder and run again. It will be recreated.
- Markdown prints without a panel
  - Install the `rich` package and make sure your virtual environment is active.

## 13. Customization

- Change the chat model
  - Edit `agent.py` and set `ChatOllama(model="...")` to a model that is already pulled on your machine.
- Remove a tool
  - Remove the corresponding import and remove it from the `tools=[...]` list in `agent.py`.
- Adjust the spinner text or color
  - Edit `utils/spinner.py`. The color codes and frames are defined at the top of the file.
- Adjust the Markdown theme or border
  - Edit `utils/markdown_render.py`. The color theme and panel style are defined in `_get_console()` and in the `Panel(...)` call.

- Change behavior of `save_md_locally`
  - Edit `tools/save_md.py`. You can change the base directory (`./LocalStore`) or filename rules.

- Change behavior of `summarize_text`
  - Edit `tools/summarize_text.py`. It uses `ChatOllama(model="gpt-oss:120b-cloud", temperature=0.4)` and formats a Markdown summary with a Key Takeaway section. Replace the model name with one you have locally if needed, or adjust the prompt.

## 14. Security and privacy

- The vector store is saved locally in `./chromadb_store`.
- Web tools send queries to external services. Review the code in `tools/` to understand what is being sent and what libraries are used.
- Do not store secrets in code. Use the `.env` file for AskNews credentials.

## 15. Limitations and notes

- Tool results come from public web sources and may change.
- The quality of answers depends on the local model and the connectivity of the tools you use.
- Large chat models may require significant memory and disk space. Choose a model that fits your machine.

## 16. Directory overview

```
LocalAgent/
├─ agent.py
├─ retriever.py
├─ requirements.txt
├─ README.md
├─ documentation.md
├─ prompts/
│  └─ research_prompt.py
├─ tools/
│  ├─ wiki.py
│  ├─ duckduckgo.py
│  ├─ arxiv_tool.py
│  ├─ math.py
│  ├─ getDate.py
│  ├─ getNews.py
│  ├─ save_md.py
│  └─ summarize_text.py
├─ store/
│  └─ chromadb.py
├─ utils/
│  ├─ spinner.py
│  └─ markdown_render.py
├─ chromadb_store/    # created at runtime
└─ tests/
   ├─ test_math.py
   ├─ test_wiki.py
   ├─ test_duckduckgo.py
   ├─ test_arxiv.py
   └─ test_asknews.py
```

## 17. Questions and answers

**How do I change the model quickly?**  
Open `agent.py` and edit the `ChatOllama(model=...)` line. Pull that model with Ollama before running.

**How do I reset memory?**  
Delete the `chromadb_store` folder.

**Can I run without AskNews?**  
Yes. Remove the AskNews import and remove the tool from the `tools=[...]` list in `agent.py`.

**The Markdown panel does not appear.**  
Install `rich` and make sure your virtual environment is active. If Rich is missing, the app prints plain text instead.

**Where are errors printed?**  
Each tool returns a short error message string on failure. The spinner line shows a failure mark and duration. Check the terminal output.

---

This document should provide enough detail to set up, run, understand, and customize the project without reading the source code first. Refer to the file paths above if you want to change behavior.
