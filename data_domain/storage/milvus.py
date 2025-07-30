"""
Milvus vector storage utilities.
"""
from typing import List
from pymilvus import Collection, connections
from ..utils import config

def connect_milvus() -> None:
    """
    Connect to Milvus server.

    >>> connect_milvus()  # doctest: +SKIP
    """
    connections.connect(host=config.MILVUS_HOST, port=config.MILVUS_PORT)

def insert_embeddings(embeddings: List[List[float]], ids: List[int]) -> None:
    """
    Insert embeddings into Milvus collection.

    >>> insert_embeddings([[0.1]*128], [1])  # doctest: +SKIP
    """
    connect_milvus()
    collection = Collection(config.COLLECTION_NAME)
    data = [ids, embeddings]
    collection.insert(data)