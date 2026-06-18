import os

from dotenv import load_dotenv
from groq import Groq

from sql_rag.schema import (
    DATABASE_SCHEMA
)

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_sql(question):

    prompt = f"""
You are an expert SQLite SQL generator.

Database Schema:

{DATABASE_SCHEMA}

Rules:

1. Generate ONLY valid SQLite SELECT queries.
2. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE.
3. Use only tables and columns from the schema.
4. Return SQL only.
5. Do not use markdown.
6. Do not explain anything.

Question:

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

    sql = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )

    return sql


if __name__ == "__main__":

    question = (
        "How many claims are pending?"
    )

    sql = generate_sql(question)

    print(sql)