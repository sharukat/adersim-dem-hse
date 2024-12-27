import unittest
from unittest.mock import patch, MagicMock
import os
import numpy as np

class TestSemanticCache(unittest.TestCase):
    @patch("src.utils.retrieve_cache", return_value={
        "questions": [], "embeddings": [], "responses": [], "urls": []
    })
    def setUp(self, mock_retrieve):
        """Set up test fixtures before each test method."""
        # Test data
        self.test_cache_file = "cache.json"
        self.test_question = "What is AI?"
        self.test_response = "AI stands for Artificial Intelligence."
        self.test_urls = [["https://example.com/ai", "https://sharuka.com/ai"]]
        self.test_embedding = np.array([0.1] * 768, dtype=np.float32)

        # Mock FAISS index
        self.mock_index = MagicMock()
        self.mock_index.search.return_value = (np.array([[0.2]]), np.array([[0]]))

        # Mock the encoder
        self.mock_encoder = MagicMock()
        self.mock_encoder.encode.return_value = np.array([self.test_embedding])
        
        # Create patcher for SentenceTransformer
        self.encoder_patcher = patch(
            'sentence_transformers.SentenceTransformer',
            return_value=self.mock_encoder
        )
        self.encoder_mock = self.encoder_patcher.start()

        # Create patcher for FAISS index
        self.faiss_patcher = patch('faiss.IndexFlatL2', return_value=self.mock_index)
        self.faiss_mock = self.faiss_patcher.start()

        # Create cache instance
        from src.cache import SemanticCache
        self.cache = SemanticCache(
            file=self.test_cache_file,
            max_size=3,
            threshold=0.35,
            evict_policy="FIFO"
        )

    def tearDown(self):
        """Clean up after each test method."""
        self.encoder_patcher.stop()
        self.faiss_patcher.stop()
        if os.path.exists(self.test_cache_file):
            os.remove(self.test_cache_file)

    def test_initialization(self):
        """Test if cache is initialized with correct parameters."""
        self.assertEqual(self.cache.file, self.test_cache_file)
        self.assertEqual(self.cache.max_size, 3)
        self.assertEqual(self.cache.threshold, 0.35)
        self.assertEqual(self.cache.evict_policy, "FIFO")
        self.assertEqual(self.cache.cache, {
            "questions": [],
            "embeddings": [],
            "responses": [],
            "urls": []
        })

    @patch("src.utils.store_cache")
    @patch("src.utils.deque_list")
    def test_add_to_cache(self, mock_deque, mock_store):
        """Test adding an item to cache."""
        # Mock deque behavior
        mock_deque.return_value = [self.test_question]

        # Add item to cache
        self.cache.add_to_cache(self.test_question, self.test_response, self.test_urls)

        # Verify encoder was called
        self.mock_encoder.encode.assert_called_once_with([self.test_question])

        # Verify cache contents
        self.assertEqual(len(self.cache.cache["questions"]), 1)
        self.assertEqual(len(self.cache.cache["responses"]), 1)
        self.assertEqual(len(self.cache.cache["urls"]), 1)
        self.assertEqual(self.cache.cache["questions"][0], self.test_question)
        self.assertEqual(self.cache.cache["responses"][0], self.test_response)
        self.assertEqual(self.cache.cache["urls"][0], self.test_urls)
        
        # Verify store_cache was called
        mock_store.assert_called_once_with(self.test_cache_file, self.cache.cache)

    def test_search_empty_cache(self):
        """Test search functionality with empty cache."""
        result = self.cache.search("test query")
        self.assertIsNone(result)

    def test_search_with_match(self):
        """Test search functionality with matching item in cache."""
        # Set up cache data
        self.cache.cache = {
            "questions": [self.test_question],
            "embeddings": [self.test_embedding.tolist()],
            "responses": [self.test_response],
            "urls": [self.test_urls]
        }
        
        # Set up mock index to return a close match
        self.mock_index.search.return_value = (np.array([[0.2]]), np.array([[0]]))
        
        # Perform search
        result = self.cache.search(self.test_question)
        
        # Verify the search was performed correctly
        self.mock_encoder.encode.assert_called_with([self.test_question])
        self.assertEqual(result, self.test_response)

    def test_search_without_match(self):
        """Test search functionality when no match is found."""
        # Set up cache data
        self.cache.cache = {
            "questions": [self.test_question],
            "embeddings": [self.test_embedding.tolist()],
            "responses": [self.test_response],
            "urls": [self.test_urls]
        }
        
        # Set up mock index to return a distant match (above threshold)
        self.mock_index.search.return_value = (np.array([[0.5]]), np.array([[0]]))
        
        # Perform search
        result = self.cache.search("different question")
        
        # Verify no match was found
        self.assertIsNone(result)

    @patch("src.utils.store_cache")
    @patch("src.utils.deque_list")
    def test_cache_eviction(self, mock_deque, mock_store):
        """Test if cache eviction works when max size is reached."""
        # Mock deque_list to implement FIFO behavior
        def fifo_deque(lst, max_size):
            return lst[-max_size:] if len(lst) > max_size else lst
        mock_deque.side_effect = fifo_deque

        # Add items up to max size + 1
        for i in range(4):
            self.cache.add_to_cache(
                f"Question {i}",
                f"Response {i}",
                [[f"URL {i}"]]
            )

        # Verify cache size doesn't exceed max_size
        self.assertEqual(len(self.cache.cache["questions"]), 3)
        self.assertEqual(len(self.cache.cache["responses"]), 3)
        self.assertEqual(len(self.cache.cache["urls"]), 3)
        
        # Verify the oldest item was evicted (FIFO)
        self.assertNotIn("Question 0", self.cache.cache["questions"])
        self.assertIn("Question 3", self.cache.cache["questions"])


if __name__ == "__main__":
    unittest.main()
