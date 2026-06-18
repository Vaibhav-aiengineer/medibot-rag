import json

from qdrant_client.models import PointStruct

from vectorstore.client_manager import get_qdrant_client
from vectorstore.qdrant_store import create_collection
from retrieval.encoders import (
    COLLECTION_NAME,
    DENSE_VECTOR,
    SPARSE_VECTOR,
    embed_dense,
    embed_sparse,
)


def main():

    print("Recreating collection...")
    create_collection()

    print("Loading chunks...")
    with open("data/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"Found {len(chunks)} chunks")

    points = []

    for index, chunk in enumerate(chunks):

        text = chunk["text"]

        points.append(
            PointStruct(
                id=chunk["id"],
                vector={
                    DENSE_VECTOR: embed_dense(text),
                    SPARSE_VECTOR: embed_sparse(text),
                },
                payload={
                    "text": text,
                    **chunk["metadata"],
                },
            )
        )

        if (index + 1) % 50 == 0:
            print(f"  Encoded {index + 1} chunks")

    print("Uploading vectors...")

    client = get_qdrant_client()

    try:
        client.upsert(
            collection_name=COLLECTION_NAME,
            points=points,
        )
    finally:
        client.close()

    print(f"Upload complete: {len(points)} points")


if __name__ == "__main__":
    main()
