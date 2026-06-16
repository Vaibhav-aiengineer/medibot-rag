import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_answer(question, chunks):

    context = ""

    sources = set()

    for chunk in chunks:

        source = chunk["metadata"]["document"]

        sources.add(source)

        context += (
            f"[Source: {source}]\n"
            f"{chunk['text']}\n\n"
        )

    prompt = f"""
You are a hospital assistant.

Answer ONLY using the provided context.

If the answer is not present in the context,
say:

"I could not find this information in the knowledge base."

CONTEXT:

{context}

QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "sources": list(sources)
    }