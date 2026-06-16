from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

client = QdrantClient(
    path="./qdrant_data"
)

client.recreate_collection(
    collection_name="medibot",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

print("Collection Created")

client.close()