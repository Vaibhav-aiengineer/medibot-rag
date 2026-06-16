from retrieval.rag_retriever import retrieve
from llm.generator import generate_answer

role = input(
    "Role (doctor/nurse/billing/admin/technician): "
).lower()

while True:

    question = input(
        "\nAsk a question (q to quit): "
    )

    if question.lower() == "q":

        print("\nGoodbye!")

        break

    chunks = retrieve(
        question=question,
        role=role,
        top_k=5
    )

    result = generate_answer(
        question,
        chunks
    )

    print("\nANSWER:\n")

    print(result["answer"])

    if result["sources"]:

        print("\nSOURCES:\n")

        for source in result["sources"]:

            print(f"- {source}")