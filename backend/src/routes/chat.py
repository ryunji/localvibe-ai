from fastapi import APIRouter
from pydantic import BaseModel
from src.services.hf_client import ask_hf

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    q: str

@router.post("/chat")
def chat(req: ChatRequest):
    print("✅ [chat] req.q =", req.q)

    result = ask_hf(req.q)

    print("✅ [chat] result type =", type(result))
    print("✅ [chat] result value =", result)

    return result
