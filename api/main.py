from fastapi import FastAPI

from api.models import (
    ChatRequest,
    LoginRequest
)

from api.auth import DEMO_USERS
from api.roles import ROLE_COLLECTIONS

from retrieval.rag_retriever import retrieve
from llm.generator import generate_answer


app = FastAPI()


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

    chunks = retrieve(
        question=request.question,
        role=request.role,
        top_k=5
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