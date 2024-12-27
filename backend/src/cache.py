from typing import List
import faiss
from sentence_transformers import SentenceTransformer
from src.utils import retrieve_cache, deque_list, store_cache


class SemanticCache:
    def __init__(
        self,
        file: str = "cache_file.json",
        threshold: float = 0.35,
        max_size: int = 100,
        evict_policy: str = None,
        encoder_mode: str = "all-mpnet-base-v2",
    ):
        """Initializes the semantic cache.

        Args:
            file (str):
                Name of the JSON file to store the cache.
            threshold (float):
                Euclidean distance threshold for question similarity.
            max_size (int):
                Maximum number of responses the cache can store.
            evict_policy (str):
                Eviction policy ('FIFO' supported; None for no policy).
        """
        self.index = faiss.IndexFlatL2(768)
        self.encoder = SentenceTransformer(encoder_mode)
        self.threshold = threshold
        self.cache = retrieve_cache(file)
        self.max_size = max_size
        self.evict_policy = evict_policy
        self.file = file

    def evict_from_cache(self):
        """Evicts an item from the cache based on the eviction policy."""
        cache_size = len(self.cache["questions"])
        if self.evict_policy and cache_size > self.max_size:
            for key, _ in self.cache.items:
                self.cache[key] = deque_list(self.cache[key], self.max_size)

    def add_to_cache(self, question: str, response: str, urls: List[str]):
        try:
            embedding = self.encoder.encode([question])
            if self.evict_policy == "FIFO":
                cache_keys = ["questions", "embeddings", "responses", "urls"]
                new_entries = [question, embedding[0].tolist(), response, urls]

                for key, entry in zip(cache_keys, new_entries):
                    queue = deque_list(self.cache[key], self.max_size)
                    queue.append(entry)
                    self.cache[key] = list(queue)

            self.index.add(embedding)  # Add new embedding to FAISS index
            store_cache("cache.json", self.cache)
        except Exception as e:
            raise RuntimeError(f"Error adding to cache: {e}")

    def search(self, question: str) -> str:
        try:
            if len(self.cache["questions"]) == 0:
                return None
            embedding = self.encoder.encode([question])
            distances, indices = self.index.search(embedding, 1)

            # Check if the nearest neighbor is within threshold
            if indices[0][0] >= 0 and distances[0][0] <= self.threshold:
                return self.cache["responses"][indices[0][0]]
            return None
        except Exception as e:
            raise RuntimeError(f"Error during cache lookup: {e}")
