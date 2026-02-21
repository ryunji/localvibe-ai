from src.services.rag.rag_service import rag_answer

def main():
    question = "리얼장충은 어떤 곳이야?"
    answer = rag_answer(question)

    print("질문:", question)
    print("답변:", answer)

if __name__ == "__main__":
    main()