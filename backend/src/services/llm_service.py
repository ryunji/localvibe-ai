import os

MODE = os.getenv("LLM_MODE", "local")

if MODE == "local":
    from src.adapters.local_llm import ask_Hugging_face_model_qwen as ask_llm
elif MODE == "openai":
    from src.adapters.openai_llm import ask_openai as ask_llm
else:
    raise ValueError("Invalid LLM_MODE")


def ask(question: str):
    return ask_llm(question)