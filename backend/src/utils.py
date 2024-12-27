import json
from collections import deque


def store_cache(json_file, cache):
    """Saves the cache to a JSON file, creating the file if it doesn't exist.

    Args:
        json_file (str): Path to the JSON file.
        cache (dict): Data to be stored in the file.
    """
    with open(json_file, 'w') as file:
        json.dump(cache, file)


def deque_list(input_list: list, max_size: int):
    """Removes elements from the left when size exceeds the maximum.

    Args:
        input_list (list): The input list to be converted into a deque.
        max_size (int): The maximum size of the deque.

    Returns:
        deque: A queue representation of the deque.
    """
    queue = deque(input_list, maxlen=max_size)
    return queue


def retrieve_cache(file):
    """Retrieve data from a JSON file to populate the cache.

    Args:
        file (str): Path to the JSON file storing the cache.

    Returns:
        dict: A dictionary containing cached data with keys:
            - "questions" (list): Cached questions.
            - "embeddings" (list): Embedding vectors for the questions.
            - "answers" (list): Cached answers.
            - "response" (list): Text responses corresponding to the answers.
            If the file is not found, returns an empty cache structure.
    """
    try:
        with open(file, "r") as json_file:
            cache = json.load(json_file)
    except FileNotFoundError:
        cache = {
            "questions": [],
            "embeddings": [],
            "urls": [],
            "responses": []}

    return cache
