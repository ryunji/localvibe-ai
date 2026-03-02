from fastapi import APIRouter
from pydantic import BaseModel
from src.services.llm.llm_service import ask
import os

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    q: str
    model: str = "local"  # 프론트에서 "local" | "gpt" 넘어옴

@router.post("/chat")
def chat(req: ChatRequest):
    
    print("✅ [chat] req.q =", req.q)
    
    result = ask(req.q, req.model)
    print("[chat] result type =", type(result))
    print("[chat] result value =", result)
    return result
