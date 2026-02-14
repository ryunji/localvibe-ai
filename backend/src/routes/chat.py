from fastapi import APIRouter
from pydantic import BaseModel
from src.services.llm_service import ask
import os

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    q: str

@router.post("/chat")
def chat(req: ChatRequest):
    print("✅ [chat] req.q =", req.q)

    result = ask(req.q)

    print("[chat] result type =", type(result))
    print("[chat] result value =", result)

    return result
