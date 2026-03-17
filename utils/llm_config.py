"""
LLM Provider Configuration Manager

Supports multiple LLM providers:
- Ollama (local/remote)
- LM Studio
- OpenAI
- OpenAI-compatible (OpenRouter, Together.ai, Groq, etc.)
"""

import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class LLMConfig:
    """Configuration manager for LLM providers"""

    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        self.embedding_provider = os.getenv("EMBEDDING_PROVIDER", "ollama").lower()
        self.chat_model = os.getenv("CHAT_MODEL", "gpt-oss:120b-cloud")
        self.embed_model = os.getenv("EMBED_MODEL", "nomic-embed-text")
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))

    def get_chat_model(self):
        """Get configured chat model based on provider"""
        from langchain_ollama import ChatOllama
        from langchain_openai import ChatOpenAI

        if self.provider == "ollama":
            return self._get_ollama_chat()
        elif self.provider == "lmstudio":
            return self._get_lmstudio_chat()
        elif self.provider == "openai":
            return self._get_openai_chat()
        elif self.provider == "openai_compatible":
            return self._get_openai_compatible_chat()
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def get_embedding_model(self):
        """Get configured embedding model based on provider"""
        from langchain_ollama import OllamaEmbeddings
        from langchain_openai import OpenAIEmbeddings

        if self.embedding_provider == "ollama":
            return self._get_ollama_embeddings()
        elif self.embedding_provider == "lmstudio":
            return self._get_lmstudio_embeddings()
        elif self.embedding_provider == "openai":
            return self._get_openai_embeddings()
        elif self.embedding_provider == "openai_compatible":
            return self._get_openai_compatible_embeddings()
        else:
            raise ValueError(f"Unsupported embedding provider: {self.embedding_provider}")

    def _get_ollama_chat(self):
        """Configure Ollama chat model"""
        from langchain_ollama import ChatOllama

        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        api_key = os.getenv("OLLAMA_API_KEY")

        kwargs = {
            "model": self.chat_model,
            "temperature": self.temperature,
            "base_url": base_url,
        }

        if api_key:
            kwargs["api_key"] = api_key

        return ChatOllama(**kwargs)

    def _get_ollama_embeddings(self):
        """Configure Ollama embeddings"""
        from langchain_ollama import OllamaEmbeddings

        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        api_key = os.getenv("OLLAMA_API_KEY")

        kwargs = {
            "model": self.embed_model,
            "base_url": base_url,
        }

        if api_key:
            kwargs["api_key"] = api_key

        return OllamaEmbeddings(**kwargs)

    def _get_lmstudio_chat(self):
        """Configure LM Studio chat model (OpenAI-compatible)"""
        from langchain_openai import ChatOpenAI

        base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
        api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")  # LM Studio uses dummy key

        return ChatOpenAI(
            model=self.chat_model,
            temperature=self.temperature,
            base_url=base_url,
            api_key=api_key,
        )

    def _get_lmstudio_embeddings(self):
        """Configure LM Studio embeddings (OpenAI-compatible)"""
        from langchain_openai import OpenAIEmbeddings

        base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
        api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")

        return OpenAIEmbeddings(
            model=self.embed_model,
            base_url=base_url,
            api_key=api_key,
        )

    def _get_openai_chat(self):
        """Configure OpenAI chat model"""
        from langchain_openai import ChatOpenAI

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("<"):
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider")

        kwargs = {
            "model": self.chat_model,
            "temperature": self.temperature,
            "api_key": api_key,
        }

        # Optional overrides
        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url:
            kwargs["base_url"] = base_url

        organization = os.getenv("OPENAI_ORGANIZATION")
        if organization:
            kwargs["organization"] = organization

        return ChatOpenAI(**kwargs)

    def _get_openai_embeddings(self):
        """Configure OpenAI embeddings"""
        from langchain_openai import OpenAIEmbeddings

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("<"):
            raise ValueError("OPENAI_API_KEY is required for OpenAI provider")

        kwargs = {
            "model": self.embed_model,
            "api_key": api_key,
        }

        base_url = os.getenv("OPENAI_BASE_URL")
        if base_url:
            kwargs["base_url"] = base_url

        organization = os.getenv("OPENAI_ORGANIZATION")
        if organization:
            kwargs["organization"] = organization

        return OpenAIEmbeddings(**kwargs)

    def _get_openai_compatible_chat(self):
        """Configure OpenAI-compatible chat model (OpenRouter, Together.ai, Groq, etc.)"""
        from langchain_openai import ChatOpenAI

        base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL")
        api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY")

        if not base_url:
            raise ValueError("OPENAI_COMPATIBLE_BASE_URL is required for openai_compatible provider")
        if not api_key or api_key.startswith("<"):
            raise ValueError("OPENAI_COMPATIBLE_API_KEY is required for openai_compatible provider")

        # Allow override of model for provider-specific models
        model = os.getenv("OPENAI_COMPATIBLE_MODEL") or self.chat_model

        return ChatOpenAI(
            model=model,
            temperature=self.temperature,
            base_url=base_url,
            api_key=api_key,
        )

    def _get_openai_compatible_embeddings(self):
        """Configure OpenAI-compatible embeddings"""
        from langchain_openai import OpenAIEmbeddings

        base_url = os.getenv("OPENAI_COMPATIBLE_BASE_URL")
        api_key = os.getenv("OPENAI_COMPATIBLE_API_KEY")

        if not base_url:
            raise ValueError("OPENAI_COMPATIBLE_BASE_URL is required for openai_compatible provider")
        if not api_key or api_key.startswith("<"):
            raise ValueError("OPENAI_COMPATIBLE_API_KEY is required for openai_compatible provider")

        return OpenAIEmbeddings(
            model=self.embed_model,
            base_url=base_url,
            api_key=api_key,
        )


# Singleton instance
_config = None

def get_llm_config() -> LLMConfig:
    """Get or create LLM configuration singleton"""
    global _config
    if _config is None:
        _config = LLMConfig()
    return _config


def get_chat_model():
    """Convenience function to get chat model"""
    return get_llm_config().get_chat_model()


def get_embedding_model():
    """Convenience function to get embedding model"""
    return get_llm_config().get_embedding_model()
