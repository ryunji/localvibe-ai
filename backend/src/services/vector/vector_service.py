# 저장서비스
from sqlalchemy import select
from src.db.models.vector.vector_models import SessionLocal, Document
from src.services.embedding.embedding_service import embed_text

def ingest_chunks(chunk_objects: list[dict], source_name: str):
    db = SessionLocal()

    for idx, item in enumerate(chunk_objects):
        text = item["text"]   # 🔥 핵심 수정 부분

        embedding = embed_text(text)

        doc = Document(
            source=source_name,
            chunk_index=idx,
            content=text,
            embedding=embedding
        )

        db.add(doc)

    db.commit()
    db.close()


def search_similar(query: str, top_k: int = 5):
    db = SessionLocal()

    query_embedding = embed_text(query)

    results = db.execute(
        select(Document)
        .order_by(Document.embedding.cosine_distance(query_embedding))
        .limit(top_k)
    )

    docs = [r[0].content for r in results]

    db.close()
    return docs