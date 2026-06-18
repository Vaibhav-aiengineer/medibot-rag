import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def format_sql_answer(
    question,
    sql,
    result
):

    prompt = f"""
You are a healthcare analytics assistant.

Question:
{question}

SQL Query:
{sql}

SQL Result:
{result}

Generate a concise natural language answer.

Do not mention SQL.
"""

    response = (
        client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    )

    return (
        response
        .choices[0]
        .message
        .content
    )