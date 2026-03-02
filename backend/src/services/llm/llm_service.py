from src.adapters.llm.local_llm import ask_Hugging_face_model_qwen as ask_local
from src.adapters.llm.openai_llm import ask_openai

def ask(question: str, model: str = "local"):
    if model == "gpt":
        return ask_openai(question)
    else:
        return ask_local(question)