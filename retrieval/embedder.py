from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)

print("Model Loaded")

embedding = model.encode(
    "Drug: Amoxicillin"
)

print(type(embedding))
print(len(embedding))