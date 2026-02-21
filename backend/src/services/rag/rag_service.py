from src.services.vector.vector_service import search_similar
from src.services.llm_service import ask   # 네 기존 LLM 호출 함수

def rag_answer(query: str):

    # 1. 벡터 검색
    contexts = search_similar(query, top_k=3)

    if not contexts:
        return "관련 정보를 찾지 못했습니다."

    # 2. 컨텍스트 묶기
    context_text = "\n\n".join(contexts)

    # 3. 프롬프트 구성
    prompt = f"""
당신은 전시/핫스팟 정보를 안내하는 AI입니다.

아래 컨텍스트만을 기반으로 답변하세요.
컨텍스트에 없는 정보는 추측하지 마세요.

[컨텍스트]
{context_text}

[질문]
{query}

[답변]
"""

    # 4. LLM 호출
    response = ask(prompt)

    return response