from qdrant_client import QdrantClient


# Local (embedded) Qdrant storage location.
QDRANT_PATH = "./qdrant_data"


def get_qdrant_client():

    return QdrantClient(
        path=QDRANT_PATH
    )
