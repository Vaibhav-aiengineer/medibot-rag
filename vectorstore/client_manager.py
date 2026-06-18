from qdrant_client import QdrantClient


def get_qdrant_client():

    return QdrantClient(
        path="./qdrant_data"
    )