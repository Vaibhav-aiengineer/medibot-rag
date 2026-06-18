import shutil
from pathlib import Path

from qdrant_client.models import (
    Distance,
    VectorParams,
    SparseVectorParams,
    PayloadSchemaType,
)

from vectorstore.client_manager import (
    get_qdrant_client,
    QDRANT_PATH,
)
from retrieval.encoders import (
    COLLECTION_NAME,
    DENSE_SIZE,
    DENSE_VECTOR,
    SPARSE_VECTOR,
)


def create_collection():
    """
    (Re)create the hybrid collection: one named dense vector and one
    named sparse (BM25) vector per point, plus a payload index on
    access_roles so role filtering runs at the vector-store level.

    Embedded (on-disk) Qdrant does not reliably drop existing points
    via delete_collection / recreate_collection, which silently
    leaves stale vectors behind. To guarantee a clean rebuild we
    remove the storage directory before recreating the collection.
    """

    storage = Path(QDRANT_PATH)
    if storage.exists():
        shutil.rmtree(storage)

    client = get_qdrant_client()

    try:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config={
                DENSE_VECTOR: VectorParams(
                    size=DENSE_SIZE,
                    distance=Distance.COSINE,
                )
            },
            sparse_vectors_config={
                SPARSE_VECTOR: SparseVectorParams()
            },
        )

        client.create_payload_index(
            collection_name=COLLECTION_NAME,
            field_name="access_roles",
            field_schema=PayloadSchemaType.KEYWORD,
        )

        print("Collection created (dense + sparse)")

    finally:
        client.close()


if __name__ == "__main__":
    create_collection()
