from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny
)


# -----------------------------
# Models
# -----------------------------

embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

client = QdrantClient(
    path="./qdrant_data"
)


# -----------------------------
# Config
# -----------------------------

MIN_RERANK_SCORE = 1.0


# -----------------------------
# Retrieval
# -----------------------------

def retrieve(question, role, top_k=5):

    query_vector = embedding_model.encode(
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

        limit=20
    ).points


    if not results:
        return []

    pairs = [
        (question, result.payload["text"])
        for result in results
    ]

    scores = reranker.predict(pairs)

    reranked = []

    for result, score in zip(results, scores):

        reranked.append(
            {
                "score": float(score),
                "text": result.payload["text"],
                "metadata": result.payload
            }
        )

    reranked.sort(
        key=lambda x: x["score"],
        reverse=True
    )


    if reranked[0]["score"] < MIN_RERANK_SCORE:

        print(
            f"Top score below threshold "
            f"({MIN_RERANK_SCORE})"
        )

        return []

    return reranked[:top_k]


# -----------------------------
# Local Test
# -----------------------------

if __name__ == "__main__":

    question = "What is the standard dose of Amoxicillin?"

    results = retrieve(
        question=question,
        role="doctor"
    )

    for result in results:

        print("\n====================")

        print(
            f"Score: {result['score']:.4f}"
        )

        print(result["text"])

    client.close()