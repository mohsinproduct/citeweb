# File: modules/memory/vector_store.py
import chromadb
from chromadb.utils import embedding_functions
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

class CitewebMemory:
    def __init__(self):
        # 1. Hardware-Safe Embedding Function (Runs on your CPU)
        # This model is tiny (22MB) but powerful enough for citation auditing.
        self.model_name = "all-MiniLM-L6-v2"
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=self.model_name
        )

        # 2. Local Database Initialization
        # We store data in a folder so it persists even if you restart the PC.
        self.db_path = os.path.join(os.getcwd(), "chroma_db")
        self.client = chromadb.PersistentClient(path=self.db_path)
        
        # 3. Create or Get a Collection (Think of this as a 'Table' in SQL)
        self.collection = self.client.get_or_create_collection(
            name="website_citations",
            embedding_function=self.embedding_fn
        )

        # 4. Text Splitter (Logic: 500 chars with 50 char overlap to keep context)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", " "]
        )

    def save_text(self, text: str, url: str):
        """Chunks the text, vectorizes it, and saves it to the local disk."""
        if not text:
            return {"error": "No text provided for memory storage."}

        # Break the long text into smaller AI-digestible pieces
        chunks = self.splitter.split_text(text)
        
        # Create unique IDs for every chunk (e.g., https://site.com_0)
        ids = [f"{url}_{i}" for i in range(len(chunks))]
        # Metadata allows the AI to cite the exact source later
        metadatas = [{"source": url} for _ in range(len(chunks))]

        try:
            self.collection.add(
                documents=chunks,
                ids=ids,
                metadatas=metadatas
            )
            return {"status": "success", "chunks_saved": len(chunks)}
        except Exception as e:
            return {"error": str(e)}

    def search(self, query: str, n_results: int = 3):
        """Searches memory for the most relevant text chunks."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results