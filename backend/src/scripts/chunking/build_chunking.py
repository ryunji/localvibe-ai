# backend/src/scripts/chunking/build_chunking.py

import json

from src.services.rag.parser.junggu_parser import JungguPDFParser
from src.services.rag.chunking.chunker import JungguChunker


def main():
    with open("data/processed/j.txt", encoding="utf-8") as f:
        text = f.read()

    parser = JungguPDFParser()
    pois = parser.parse(text)

    # ✅ 내부 문장까지 정밀 검색: sentence or window 추천
    chunker = JungguChunker(mode="sentence", min_chars=40)
    chunks = chunker.build(pois)

    # ✅ JSON처럼 눈에 보이게
    payload = [c.to_dict() for c in chunks]
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    # 원하면 파일 저장
    with open("data/processed/j_chunks.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()