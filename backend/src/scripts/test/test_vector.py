# 청킹된 데이터를 DB에 저장한다.
import json
from src.services.vector.vector_service import ingest_chunks

FILE_PATH = "data/processed/j_chunks.json"

def main():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    print(f"총 {len(chunks)}개 청크 발견")

    ingest_chunks(chunks, source_name="j")

    print("🔥 벡터 DB 저장 완료")

if __name__ == "__main__":
    main()