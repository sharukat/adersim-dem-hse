import pytest
from unittest.mock import patch
from src.cache import SemanticCache


@pytest.fixture
def mock_retrieve_cache():
    """Fixture to mock the retrieve_cache function."""
    with patch("src.utils.retrieve_cache", return_value={
        "questions": [],
        "embeddings": [],
        "responses": [],
        "urls": []
    }) as mock_cache:
        yield mock_cache


@pytest.fixture
def init_cache():
    """Fixture to initialize the SemanticCache with real dependencies."""
    return SemanticCache(
        file="test_cache.json",
        threshold=0.35,
        max_size=3,
        evict_policy="FIFO"
    )


def test_init(mock_retrieve_cache):
    """Test if the SemanticCache is initialized with correct
    parameters."""
    cache = SemanticCache(
        file="test_cache.json",
        threshold=0.35,
        max_size=3,
        evict_policy="FIFO"
    )

    assert cache.file == "test_cache.json"
    assert cache.max_size == 3
    assert cache.threshold == 0.35
    assert cache.evict_policy == "FIFO"
    assert cache.cache == {
        "questions": [],
        "embeddings": [],
        "responses": [],
        "urls": []
    }


def test_add_to_cache(init_cache):

    question = "What is the capital of Sri Lanka"
    response = "The capital of Sri Lanka is Sri Jayawardenepura Kotte"
    urls = ["www.srilanka.com", "www.colombo.lk"]

    init_cache.add_to_cache(question=question, response=response, urls=urls)

    # Verify that the cache contains the question, response, and URLs
    assert init_cache.cache["questions"] == [question]
    assert init_cache.cache["responses"] == [response]
    assert init_cache.cache["urls"] == [urls]

    # Check that the embeddings were generated and stored correctly
    assert len(init_cache.cache["embeddings"]) == 1
    assert len(init_cache.cache["embeddings"][0]) == 768

    # Ensure the embedding is a valid numeric array
    embedding = init_cache.cache["embeddings"][0]
    assert isinstance(embedding, list) or hasattr(embedding, "__array__")
