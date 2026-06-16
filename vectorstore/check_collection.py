from qdrant_client import QdrantClient

client = QdrantClient(
    path="./qdrant_data"
)

count = client.count(
    collection_name="medibot",
    exact=True
)

print(count.count)

client.close()