import json

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct


print("Connecting to Qdrant...")

client = QdrantClient(
    path="./qdrant_data"
)

print("Loading embeddings...")

with open(
    "data/embeddings.json",
    "r",
    encoding="utf-8"
) as f:

    embeddings = json.load(f)

print(f"Found {len(embeddings)} vectors")

points = []

for item in embeddings:

    points.append(
        PointStruct(
            id=item["id"],
            vector=item["embedding"],
            payload={
                "text": item["text"],
                **item["metadata"]
            }
        )
    )

print("Uploading vectors...")

client.upsert(
    collection_name="medibot",
    points=points
)

print("Upload Complete")

client.close()