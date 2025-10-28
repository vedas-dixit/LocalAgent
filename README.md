## Agent Kurama

A small local research agent that runs on your machine using LangChain + Ollama. It can search Wikipedia, DuckDuckGo, Arxiv, do quick math, keep notes in a local ChromaDB, and pull in fresh news via AskNews.
<img width="1839" height="968" alt="Banner" src="https://github.com/user-attachments/assets/2e74dd65-fb2e-4c83-8a5f-d794e3fad10b" />
### What you get

- Local LLM chat (Ollama)
- Tools: wiki, duckduckgo, arxiv, math, date
- Memory: stores/retrieves snippets in a local ChromaDB folder
- Optional: AskNews for recent events (needs free API creds)
- Utilities: save markdown locally (`save_md_locally`) and summarize long text (`summarize_text`)

---

## Quick start

1. Prereqs

- macOS or Linux (Windows WSL is fine too)
- Python 3.10+
- Ollama installed and running

2. Install Ollama

- macOS (Homebrew):

```zsh
brew install ollama
ollama serve
```

- Or grab the app: https://ollama.com

3. Pull the models this project expects

- Chat model used in `agent.py`:

```zsh
ollama pull gpt-oss:120b-cloud
```

- Embedding model used for memory in `retriever.py`:

```zsh
ollama pull nomic-embed-text
```

Note: If `gpt-oss:120b-cloud` isn’t available on your system, you can swap it for a common model like `llama3:8b` or `qwen2:7b` by editing `agent.py`:

```python
llm = ChatOllama(model="llama3:8b", temperature=0.7)
```

4. Set up the project

```zsh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

5. (Optional, but recommended) Add a .env for AskNews
   The agent imports the AskNews tool on startup. To avoid errors, add your free AskNews keys:

```env
# .env
ASKNEWS_CLIENT_ID=your_client_id
ASKNEWS_CLIENT_SECRET=your_client_secret
```

Don’t want news? Temporarily remove `asknews_search` from the `tools=[...]` list in `agent.py` and the import `from tools.getNews import asknews_search`.

6. Run it

```zsh
python agent.py
```

You’ll see a prompt:

```
Ask Kurama 🦊
```

Type a question like “Summarize the latest on diffusion models” or “What is attention?”

---

## What gets saved where

- Vector store lives in `./chromadb_store` (created automatically)
- You can wipe it by deleting that folder if you want a clean slate
- Markdown reports saved via the tool are in `./LocalStore` (created automatically)

---

## Optional: run tests

There are a few quick tests under `tests/`.

```zsh
pip install -U pytest
pytest -k "not asknews"   # skip news tests if you didn’t set .env
```

---

## Troubleshooting

- “model not found” → make sure you ran `ollama pull gpt-oss:120b-cloud` and `ollama pull nomic-embed-text`. If `gpt-oss:120b-cloud` isn’t available, switch the model in `agent.py` to something you have (e.g., `llama3:8b`).
- “AskNews Error / Missing env” → add `ASKNEWS_CLIENT_ID` and `ASKNEWS_CLIENT_SECRET` to your `.env` or remove the AskNews tool from the agent.
- “Ollama not running” → start it with `ollama serve`. On macOS, the app can also run a background service.
- “Chroma DB issues” → delete the `chromadb_store` folder and try again.

---

## What’s inside

- `agent.py` – creates the agent and wires up tools
- `retriever.py` – embeddings + ChromaDB add/query
- `tools/` – wiki, duckduckgo, arxiv, math, date, asknews, save_md, summarize_text
- `prompts/research_prompt.py` – the system prompt

![research-mode](https://media.tenor.com/8c9Kymc-A_gAAAAC/research-chill.gif)

That’s it. Keep it simple, keep it local, have fun.
