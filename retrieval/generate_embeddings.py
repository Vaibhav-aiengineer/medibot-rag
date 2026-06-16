import json

from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Model loaded")

print("Loading chunks...")

with open(
    "data/chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks")

embeddings = []

for index, chunk in enumerate(chunks):

    vector = model.encode(
        chunk["text"],
        normalize_embeddings=True
    )

    embeddings.append(
        {
            "id": chunk["id"],
            "text": chunk["text"],
            "metadata": chunk["metadata"],
            "embedding": vector.tolist()
        }
    )

    if (index + 1) % 50 == 0:
        print(f"Processed {index + 1} chunks")


with open(
    "data/embeddings.json",
    "w",
    encoding="utf-8"
) as f:

    json.dump(
        embeddings,
        f,
        ensure_ascii=False
    )

print("Embeddings saved")