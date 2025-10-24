# backend/app/services/vector_store.py
import faiss
import numpy as np
import os
import pickle

VECTOR_DIR = "/app/vector_store"

class VectorStore:
    """
    Simple FAISS-based vector store for each fund.
    Persists index and metadata to disk.
    """

    def __init__(self, index_name: str):
        os.makedirs(VECTOR_DIR, exist_ok=True)
        self.index_path = os.path.join(VECTOR_DIR, f"{index_name}.faiss")
        self.meta_path = os.path.join(VECTOR_DIR, f"{index_name}_meta.pkl")

        self.dim = 1536  # text-embedding-3-small
        self.texts = []

        if os.path.exists(self.index_path):
            try:
                self.index = faiss.read_index(self.index_path)
                try:
                    idx_d = self.index.d
                except AttributeError:
                    idx_d = None
                if idx_d and idx_d != self.dim:
                    # recreate index to avoid mismatched dims
                    self.index = faiss.IndexFlatL2(self.dim)
                    self.texts = []
                else:
                    # load texts if meta exists
                    if os.path.exists(self.meta_path):
                        with open(self.meta_path, "rb") as f:
                            self.texts = pickle.load(f)
                    else:
                        self.texts = []
            except Exception:
                self.index = faiss.IndexFlatL2(self.dim)
                self.texts = []
        else:
            self.index = faiss.IndexFlatL2(self.dim)
            self.texts = []

    def add_texts(self, texts: list[str], embeddings: list[list[float]]):
        if len(embeddings) == 0:
            return
        vectors = np.array(embeddings).astype("float32")
        if vectors.ndim != 2 or vectors.shape[1] != self.dim:
            raise ValueError(f"Embeddings dimension mismatch. Expected {self.dim}, got {vectors.shape}")
        self.index.add(vectors)
        self.texts.extend(texts)
        self._save()

    def search(self, query_emb: list[float], top_k: int = 3):
        if getattr(self.index, "ntotal", 0) == 0:
            return []
        query_vec = np.array([query_emb]).astype("float32")
        distances, indices = self.index.search(query_vec, top_k)
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.texts) and idx != -1:
                results.append({
                    "text": self.texts[idx],
                    "score": float(distances[0][i])
                })
        return results

    def _save(self):
        try:
            faiss.write_index(self.index, self.index_path)
            with open(self.meta_path, "wb") as f:
                pickle.dump(self.texts, f)
        except Exception as e:
            print(f"[WARN] Failed to save vector store: {e}")
