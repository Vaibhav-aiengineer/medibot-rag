import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# Exact fallback the model is told to return when the answer is not
# in the context. Kept as a constant so the prompt and the
# source-suppression check stay in sync.
NOT_FOUND_MESSAGE = (
    "I could not find this information in the knowledge base."
)


def generate_answer(question, chunks):

    context = ""

    sources = []

    seen = set()

    for chunk in chunks:

        metadata = chunk["metadata"]

        # Deduplicate by document + collection
        source_key = (
            metadata["document"],
            metadata["collection"]
        )

        if source_key not in seen:

            seen.add(source_key)

            sources.append(
                {
                    "source_document":
                        metadata["document"],

                    "section_title":
                        metadata.get(
                            "section_title",
                            "Unknown"
                        ),

                    "collection":
                        metadata["collection"]
                }
            )

        context += (
            f"[Source: "
            f"{metadata['document']}]\n"
            f"{chunk['text']}\n\n"
        )

    system_prompt = """You are MediBot, a professional hospital knowledge assistant.

Your job is to answer medical and hospital-related questions using ONLY the provided context.

Formatting rules:
- Write a brief summary sentence first, then provide details.
- Use **bold** for key terms, drug names, and important warnings.
- Use numbered lists (1. 2. 3.) for sequential steps or procedures.
- Use bullet points (- ) for non-sequential items or lists of options.
- Use clear headings (### ) to separate distinct topics when the answer covers multiple areas.
- Keep paragraphs short (2-3 sentences max).
- Use line breaks between sections for readability.
- Be concise — do not repeat information.

Tone:
- Professional, clear, and reassuring.
- Suitable for healthcare staff referencing hospital protocols.

If the answer is not present in the context, reply exactly:
"{NOT_FOUND_MESSAGE}"
""".format(NOT_FOUND_MESSAGE=NOT_FOUND_MESSAGE)

    user_prompt = f"""CONTEXT:

{context}

QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    # Don't cite sources for a non-answer: when the model reports it
    # could not find the information, showing a source is misleading.
    if NOT_FOUND_MESSAGE.lower() in (answer or "").lower():
        sources = []

    return {
        "answer": answer,
        "sources": sources
    }