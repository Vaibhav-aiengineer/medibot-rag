from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.models import (
    ChatRequest,
    LoginRequest
)

from api.auth import DEMO_USERS
from api.roles import ROLE_COLLECTIONS

from retrieval.rag_retriever import retrieve
from llm.generator import generate_answer

from sql_rag.query_router import (
    is_sql_question
)

from sql_rag.access_control import (
    can_use_sql
)

from sql_rag.text_to_sql import (
    run_text_to_sql
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/login")
def login(request: LoginRequest):

    user = DEMO_USERS.get(
        request.username
    )

    if not user:

        return {
            "success": False,
            "message": "Invalid username"
        }

    if user["password"] != request.password:

        return {
            "success": False,
            "message": "Invalid password"
        }

    return {

        "success": True,

        "token":
            f"{user['role']}_token",

        "role":
            user["role"]
    }


@app.get("/collections/{role}")
def get_collections(role: str):

    collections = ROLE_COLLECTIONS.get(role)

    if not collections:

        return {
            "success": False,
            "message": "Invalid role"
        }

    return {
        "success": True,
        "role": role,
        "collections": collections
    }


@app.post("/chat")
def chat(request: ChatRequest):

    # ==================================
    # SQL RAG PATH
    # ==================================

    if is_sql_question(
        request.question
    ):

        if not can_use_sql(
            request.role
        ):

            return {
                "answer":
                    f"As a {request.role}, "
                    f"you do not have access to "
                    f"analytical claim data.",

                "sources": [],

                "retrieval_type":
                    "sql_rag",

                "role":
                    request.role
            }

        try:

            sql_result = run_text_to_sql(
                request.question
            )

            return {

                "answer":
                    sql_result["answer"],

                "sources": [],

                "retrieval_type":
                    "sql_rag",

                "role":
                    request.role,

                "generated_sql":
                    sql_result["sql"]
            }

        except Exception as e:

            return {

                "answer":
                    f"SQL Error: {str(e)}",

                "sources": [],

                "retrieval_type":
                    "sql_rag",

                "role":
                    request.role
            }

    # ==================================
    # HYBRID RAG PATH
    # ==================================

    chunks = retrieve(
        question=request.question,
        role=request.role,
        top_k=3
    )

    if not chunks:

        return {

            "answer":
                "I could not find this information in the knowledge base.",

            "sources": [],

            "retrieval_type":
                "hybrid_rag",

            "role":
                request.role
        }

    result = generate_answer(
        request.question,
        chunks
    )

    return {

        "answer":
            result["answer"],

        "sources":
            result["sources"],

        "retrieval_type":
            "hybrid_rag",

        "role":
            request.role
    }