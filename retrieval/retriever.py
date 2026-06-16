from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient

print("Loading model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

client = QdrantClient(
    path="./qdrant_data"
)

question = "What is the standard dose of Amoxicillin?"

print(f"\nQuestion: {question}")

query_vector = model.encode(
    question,
    normalize_embeddings=True
).tolist()

results = client.query_points(
    collection_name="medibot",
    query=query_vector,
    limit=5
).points

print(f"\nFound {len(results)} results\n")

for i, result in enumerate(results, start=1):

    print("=" * 60)

    print(f"Rank: {i}")
    print(f"Score: {result.score:.4f}")

    print("\nText:")
    print(result.payload["text"][:500])

client.close()