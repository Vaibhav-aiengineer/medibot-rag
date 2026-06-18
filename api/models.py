from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str
    role: str


class LoginRequest(BaseModel):
    username: str
    password: str