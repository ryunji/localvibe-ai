# backend/src/services/rag/chunking/schema.py : 삭제하면 안됨.

from dataclasses import dataclass, asdict
from typing import Dict, Optional


@dataclass
class POIChunk:
    """
    검색용 최소 단위 청크.
    - text: 벡터/키워드 검색에 넣을 본문
    - meta: 필터/출처/추적용 메타데이터
    """
    chunk_id: str
    text: str
    meta: Dict[str, str]

    def to_dict(self):
        return asdict(self)