"""
Shared embedding configuration for indexing and retrieval.

Both the index-time and query-time paths import from here so the
dense and sparse models can never drift apart.
"""

from functools import lru_cache

from sentence_transformers import SentenceTransformer
from fastembed import SparseTextEmbedding
from qdrant_client.models import SparseVector


COLLECTION_NAME = "medibot"

DENSE_MODEL_NAME = "BAAI/bge-small-en-v1.5"
DENSE_SIZE = 384

# BM25 sparse vectors computed locally by FastEmbed and stored in
# Qdrant, so keyword (sparse) and semantic (dense) search live in one
# collection and are fused server-side at query time.
SPARSE_MODEL_NAME = "Qdrant/bm25"

DENSE_VECTOR = "dense"
SPARSE_VECTOR = "sparse"


@lru_cache(maxsize=1)
def get_dense_model():
    return SentenceTransformer(DENSE_MODEL_NAME)


@lru_cache(maxsize=1)
def get_sparse_model():
    return SparseTextEmbedding(model_name=SPARSE_MODEL_NAME)


def embed_dense(text):
    return get_dense_model().encode(
        text,
        normalize_embeddings=True,
    ).tolist()


def embed_sparse(text):
    embedding = next(get_sparse_model().embed([text]))

    return SparseVector(
        indices=embedding.indices.tolist(),
        values=embedding.values.tolist(),
    )
