import json
import re

from rank_bm25 import BM25Okapi


# ----------------------------------
# Load Chunks
# ----------------------------------

with open(
    "data/chunks.json",
    "r",
    encoding="utf-8"
) as f:

    chunks = json.load(f)


# ----------------------------------
# Build Corpus
# ----------------------------------

corpus = [
    chunk["text"]
    for chunk in chunks
]

tokenized_corpus = [

    re.findall(
        r"\b\w+\b",
        text.lower()
    )

    for text in corpus
]


# ----------------------------------
# Build BM25 Index
# ----------------------------------

bm25 = BM25Okapi(
    tokenized_corpus
)


# ----------------------------------
# BM25 Retrieval
# ----------------------------------

def retrieve_bm25(
    question,
    role,
    top_k=20
):

    query_tokens = re.findall(
        r"\b\w+\b",
        question.lower()
    )

    scores = bm25.get_scores(
        query_tokens
    )

    ranked = sorted(
        zip(chunks, scores),
        key=lambda x: x[1],
        reverse=True
    )

    results = []

    for chunk, score in ranked:

        roles = chunk["metadata"][
            "access_roles"
        ]

        if role not in roles:
            continue

        results.append(
            {
                "score": float(score),
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            }
        )

        if len(results) == top_k:
            break

    return results


# ----------------------------------
# Local Test
# ----------------------------------

if __name__ == "__main__":

    results = retrieve_bm25(
        question="What is the billing code for pneumonia?",
        role="billing",
        top_k=5
    )

    print(
        f"\nTotal Results: {len(results)}"
    )

    for result in results:

        print("\n=================")

        print(
            f"Score: {result['score']:.4f}"
        )

        print(result["text"])