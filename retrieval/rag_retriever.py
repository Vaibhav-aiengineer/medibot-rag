from sentence_transformers import (
    SentenceTransformer,
    CrossEncoder
)

from vectorstore.client_manager import (
    get_qdrant_client
)
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny
)

from retrieval.bm25_retriever import (
    retrieve_bm25
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



# -----------------------------
# Config
# -----------------------------

MIN_RERANK_SCORE = 1.0


# -----------------------------
# Retrieval
# -----------------------------

def retrieve(question, role, top_k=5):

    client = get_qdrant_client()

    try:

        # ----------------------------------
        # Dense Retrieval (Qdrant)
        # ----------------------------------

        query_vector = embedding_model.encode(
            question,
            normalize_embeddings=True
        ).tolist()

        qdrant_results = client.query_points(
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

        dense_results = []

        for result in qdrant_results:

            dense_results.append(
                {
                    "text": result.payload["text"],
                    "metadata": result.payload
                }
            )

        # ----------------------------------
        # BM25 Retrieval
        # ----------------------------------

        bm25_results = retrieve_bm25(
            question=question,
            role=role,
            top_k=20
        )

        # ----------------------------------
        # Merge Results
        # ----------------------------------

        combined_results = (
            dense_results +
            bm25_results
        )

        # ----------------------------------
        # Remove Duplicates
        # ----------------------------------

        seen = set()

        unique_results = []

        for result in combined_results:

            text = result["text"]

            if text in seen:
                continue

            seen.add(text)

            unique_results.append(result)

        if not unique_results:
            return []

        print(
            f"Dense Results: {len(dense_results)}"
        )

        print(
            f"BM25 Results: {len(bm25_results)}"
        )

        print(
            f"Unique Results: {len(unique_results)}"
        )

        # ----------------------------------
        # Reranking
        # ----------------------------------

        pairs = [

            (
                question,
                result["text"]
            )

            for result in unique_results
        ]

        scores = reranker.predict(
            pairs
        )

        reranked = []

        for result, score in zip(
            unique_results,
            scores
        ):

            reranked.append(
                {
                    "score": float(score),
                    "text": result["text"],
                    "metadata":
                        result["metadata"]
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

    finally:

        client.close()