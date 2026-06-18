from sentence_transformers import CrossEncoder

from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchAny,
    Prefetch,
    FusionQuery,
    Fusion,
)

from vectorstore.client_manager import get_qdrant_client
from retrieval.encoders import (
    COLLECTION_NAME,
    DENSE_VECTOR,
    SPARSE_VECTOR,
    embed_dense,
    embed_sparse,
)


# -----------------------------
# Models
# -----------------------------

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


# -----------------------------
# Config
# -----------------------------

# Hybrid retrieval casts a wide net (broad candidate set), then the
# cross-encoder narrows it down before anything reaches the LLM.
CANDIDATE_LIMIT = 10
RERANK_TOP_K = 3


def _role_filter(role):
    return Filter(
        must=[
            FieldCondition(
                key="access_roles",
                match=MatchAny(any=[role, "all"]),
            )
        ]
    )


def retrieve(question, role, top_k=RERANK_TOP_K):

    client = get_qdrant_client()

    try:

        # ----------------------------------
        # Hybrid retrieval in a single query:
        # dense + sparse (BM25) prefetches fused server-side (RRF).
        # The access_roles filter is applied at the vector-store
        # level on both branches.
        # ----------------------------------

        role_filter = _role_filter(role)

        response = client.query_points(
            collection_name=COLLECTION_NAME,
            prefetch=[
                Prefetch(
                    query=embed_dense(question),
                    using=DENSE_VECTOR,
                    filter=role_filter,
                    limit=CANDIDATE_LIMIT,
                ),
                Prefetch(
                    query=embed_sparse(question),
                    using=SPARSE_VECTOR,
                    filter=role_filter,
                    limit=CANDIDATE_LIMIT,
                ),
            ],
            query=FusionQuery(fusion=Fusion.RRF),
            query_filter=role_filter,
            limit=CANDIDATE_LIMIT,
            with_payload=True,
        ).points

        if not response:
            return []

        candidates = [
            {
                "text": point.payload["text"],
                "metadata": point.payload,
            }
            for point in response
        ]

        # ----------------------------------
        # Reranking: score each candidate jointly with the query,
        # then keep only the top-k for the LLM.
        # ----------------------------------

        pairs = [
            (question, candidate["text"])
            for candidate in candidates
        ]

        scores = reranker.predict(pairs)

        reranked = [
            {
                "score": float(score),
                "text": candidate["text"],
                "metadata": candidate["metadata"],
            }
            for candidate, score in zip(candidates, scores)
        ]

        reranked.sort(key=lambda x: x["score"], reverse=True)

        # No score cutoff: the cross-encoder's logits are not
        # calibrated to an absolute threshold (valid medical answers
        # frequently score negative). Grounding is enforced
        # downstream by the generator, which answers only from the
        # supplied context. We simply pass the reranked top-k.
        return reranked[:top_k]

    finally:
        client.close()
