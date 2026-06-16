from search import search

question = "What is the standard dose of Amoxicillin?"

results = search(
    question=question,
    role="billing",
    top_k=5
)

print(f"Results: {len(results)}")

for result in results:

    print("\n----------------")

    print(
        result.payload["document"]
    )

    print(
        result.payload["text"][:200]
    )