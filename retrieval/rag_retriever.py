from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)

from qdrant_client import QdrantClient


embedding_model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

client = QdrantClient(
    path="./qdrant_data"
)

def retrieve(question, top_k=5):

    query_vector = embedding_model.encode(
        question,
        normalize_embeddings=True
    ).tolist()

    results = client.query_points(
        collection_name="medibot",
        query=query_vector,
        limit=20
    ).points

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

    return reranked[:top_k]

if __name__ == "__main__":

    question = "What is the standard dose of Amoxicillin?"

    results = retrieve(question)

    for result in results:

        print("\n===================")

        print(result["score"])

        print(result["text"])

    client.close()