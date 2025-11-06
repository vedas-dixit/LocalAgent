from langchain_ollama import OllamaEmbeddings
from store.chromadb import collection
from langchain.tools import tool
import uuid
from utils.spinner import Spinner
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Ollama embeddings from environment variables
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ollama_embed_model = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

embed = OllamaEmbeddings(
    model=ollama_embed_model,
    base_url=ollama_base_url
)

@tool
def add_to_db(text: str, metadata: dict = None):
    """Add new text to the vector DB."""
    s = Spinner("Running add_to_db…")
    s.start()
    try:
        doc_id = str(uuid.uuid4())
        embedding = embed.embed_query(text)
        collection.add(
            ids=[doc_id],
            embeddings=[embedding],
            documents=[text],
            metadatas=[metadata if metadata else {"source": "manual_entry"}]
        )
        s.stop(success=True)
        return doc_id
    except Exception as e:
        s.stop(success=False)
        return f"Error: {e}"

@tool
def query_db(query: str, top_k: int = 3):
    """Retrieve the most relevant chunks for a given query."""
    s = Spinner("Running query_db…")
    s.start()
    try:
        embedding = embed.embed_query(query)
        results = collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )
        docs = results.get("documents", [[]])[0]
        s.stop(success=True)
        return "\n\n".join(docs) if docs else "No relevant context found."
    except Exception as e:
        s.stop(success=False)
        return f"Error: {e}"
