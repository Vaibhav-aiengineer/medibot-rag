from retrieval.rag_retriever import retrieve
from llm.generator import generate_answer


question = "What is the standard dose of Amoxicillin?"


chunks = retrieve(
    question,
    top_k=5
)

result = generate_answer(
    question,
    chunks
)

print("\nANSWER:\n")

print(result["answer"])

print("\nSOURCES:\n")

for source in result["sources"]:

    print(source)