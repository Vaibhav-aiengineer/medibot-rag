from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny
)

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

client = QdrantClient(
    path="./qdrant_data"
)


def search(question, role, top_k=5):

    query_vector = model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = client.query_points(
        collection_name="medibot",

        query=query_vector,

        query_filter=Filter(
            must=[
                FieldCondition(
                    key="access_roles",
                    match=MatchAny(
                        any=[role]
                    )
                )
            ]
        ),

        limit=top_k
    ).points

    return results