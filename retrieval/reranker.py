from sentence_transformers import CrossEncoder

print("Loading reranker...")

reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)

question = "What is the standard dose of Amoxicillin?"

chunks = [

    """
    Drug: Amoxicillin
    Class: Penicillin
    Standard Dose: 500 mg TDS
    """,

    """
    Regimen: Amoxicillin 500 mg TDS
    Duration: 5 days
    """
]

pairs = [
    (question, chunk)
    for chunk in chunks
]

scores = reranker.predict(pairs)

for chunk, score in zip(chunks, scores):

    print("\n===================")

    print(f"Score: {score:.4f}")

    print(chunk)