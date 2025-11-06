# LLM Provider Configuration Examples

This guide shows you how to configure different LLM providers with PersonalAgent.

## Supported Providers

1. **Ollama** (local/remote)
2. **LM Studio** (local)
3. **OpenAI** (API)
4. **OpenAI-Compatible** (OpenRouter, Together.ai, Groq, Fireworks, etc.)

## Quick Start

1. Copy `.env.template` to `.env`
2. Set your `LLM_PROVIDER` and configure the relevant section
3. Run the agent!

---

## Configuration Examples

### 1. Ollama (Local)

Default setup for local Ollama installation:

```bash
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

CHAT_MODEL=gpt-oss:120b-cloud
EMBED_MODEL=nomic-embed-text
TEMPERATURE=0.7

OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_API_KEY=  # Leave empty for local
```

### 2. Ollama (Remote/API)

Connect to a remote Ollama instance:

```bash
LLM_PROVIDER=ollama
EMBEDDING_PROVIDER=ollama

CHAT_MODEL=llama3.1:70b
EMBED_MODEL=nomic-embed-text
TEMPERATURE=0.7

OLLAMA_BASE_URL=http://your-server.com:11434
OLLAMA_API_KEY=your_api_key_if_needed
```

### 3. LM Studio (Local)

Use LM Studio's local server:

```bash
LLM_PROVIDER=lmstudio
EMBEDDING_PROVIDER=lmstudio

CHAT_MODEL=llama-3.1-8b  # Or whatever model you have loaded
EMBED_MODEL=nomic-embed-text
TEMPERATURE=0.7

LMSTUDIO_BASE_URL=http://localhost:1234/v1
LMSTUDIO_API_KEY=  # LM Studio uses a dummy key
```

**Note:** Make sure LM Studio's local server is running before starting the agent.

### 4. OpenAI

Use OpenAI's official API:

```bash
LLM_PROVIDER=openai
EMBEDDING_PROVIDER=openai

CHAT_MODEL=gpt-4o
EMBED_MODEL=text-embedding-3-small
TEMPERATURE=0.7

OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional
OPENAI_ORGANIZATION=  # Optional
```

### 5. OpenRouter

Use OpenRouter to access multiple models:

```bash
LLM_PROVIDER=openai_compatible
EMBEDDING_PROVIDER=openai_compatible

CHAT_MODEL=anthropic/claude-3.5-sonnet
EMBED_MODEL=text-embedding-3-small
TEMPERATURE=0.7

OPENAI_COMPATIBLE_BASE_URL=https://openrouter.ai/api/v1
OPENAI_COMPATIBLE_API_KEY=sk-or-v1-your-api-key
```

**Popular OpenRouter models:**
- `anthropic/claude-3.5-sonnet`
- `meta-llama/llama-3.1-405b-instruct`
- `google/gemini-pro-1.5`
- `openai/gpt-4o`

### 6. Together.ai

Use Together.ai for fast inference:

```bash
LLM_PROVIDER=openai_compatible
EMBEDDING_PROVIDER=openai_compatible

CHAT_MODEL=meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo
EMBED_MODEL=togethercomputer/m2-bert-80M-8k-retrieval
TEMPERATURE=0.7

OPENAI_COMPATIBLE_BASE_URL=https://api.together.xyz/v1
OPENAI_COMPATIBLE_API_KEY=your_together_api_key
```

### 7. Groq

Use Groq for ultra-fast inference:

```bash
LLM_PROVIDER=openai_compatible
EMBEDDING_PROVIDER=openai  # Groq doesn't have embeddings, use OpenAI

CHAT_MODEL=llama-3.1-70b-versatile
EMBED_MODEL=text-embedding-3-small
TEMPERATURE=0.7

OPENAI_COMPATIBLE_BASE_URL=https://api.groq.com/openai/v1
OPENAI_COMPATIBLE_API_KEY=gsk_your_groq_api_key

# For embeddings
OPENAI_API_KEY=sk-your-openai-api-key
```

**Popular Groq models:**
- `llama-3.1-70b-versatile`
- `llama-3.1-8b-instant`
- `mixtral-8x7b-32768`
- `gemma2-9b-it`

### 8. Fireworks.ai

Use Fireworks.ai for fast model hosting:

```bash
LLM_PROVIDER=openai_compatible
EMBEDDING_PROVIDER=openai_compatible

CHAT_MODEL=accounts/fireworks/models/llama-v3p1-70b-instruct
EMBED_MODEL=nomic-ai/nomic-embed-text-v1.5
TEMPERATURE=0.7

OPENAI_COMPATIBLE_BASE_URL=https://api.fireworks.ai/inference/v1
OPENAI_COMPATIBLE_API_KEY=fw_your_fireworks_api_key
```

### 9. Mixed Providers

You can use different providers for chat and embeddings:

```bash
# Use Groq for fast chat, OpenAI for embeddings
LLM_PROVIDER=openai_compatible
EMBEDDING_PROVIDER=openai

CHAT_MODEL=llama-3.1-70b-versatile
EMBED_MODEL=text-embedding-3-small
TEMPERATURE=0.7

# Groq for chat
OPENAI_COMPATIBLE_BASE_URL=https://api.groq.com/openai/v1
OPENAI_COMPATIBLE_API_KEY=gsk_your_groq_api_key

# OpenAI for embeddings
OPENAI_API_KEY=sk-your-openai-api-key
```

---

## Model Recommendations

### Chat Models

**For Quality:**
- `gpt-4o` (OpenAI)
- `claude-3.5-sonnet` (OpenRouter)
- `llama-3.1-405b-instruct` (OpenRouter/Together.ai)

**For Speed:**
- `llama-3.1-8b-instant` (Groq)
- `llama-3.1-70b-versatile` (Groq)
- `mixtral-8x7b-32768` (Groq)

**For Local:**
- `llama3.1:70b` (Ollama)
- `mistral:7b` (Ollama)
- `qwen2.5:32b` (Ollama)

### Embedding Models

**OpenAI:**
- `text-embedding-3-small` (fast, cheap)
- `text-embedding-3-large` (best quality)

**Local (Ollama):**
- `nomic-embed-text` (recommended)
- `mxbai-embed-large`
- `all-minilm`

---

## Troubleshooting

### "Connection refused" errors
- Check that your local server (Ollama/LM Studio) is running
- Verify the BASE_URL is correct
- Check firewall settings

### "Invalid API key" errors
- Double-check your API key is correct
- Make sure there are no extra spaces
- Verify the API key has proper permissions

### "Model not found" errors
- Ensure the model name matches exactly (case-sensitive)
- For Ollama: run `ollama list` to see available models
- For LM Studio: check the model is loaded in the UI

### Import errors
- Run `pip install -r requirements.txt` to install all dependencies
- Make sure `langchain-openai` is installed for OpenAI-compatible providers

---

## Cost Considerations

**Free/Local:**
- Ollama (local)
- LM Studio (local)

**Pay-as-you-go:**
- OpenAI: $$$ (most expensive, best quality)
- OpenRouter: $$ (varies by model)
- Together.ai: $ (affordable, fast)
- Groq: $ (very fast, affordable)
- Fireworks.ai: $ (affordable)

**Tip:** Start with Groq's free tier or use local Ollama for development!
