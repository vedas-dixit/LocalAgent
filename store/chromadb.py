import os
import chromadb
from chromadb.config import Settings

PERSIST_DIR = "./chromadb_store"
os.makedirs(PERSIST_DIR, exist_ok=True)

chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)


collection = chroma_client.get_or_create_collection(name="kurama_research")
