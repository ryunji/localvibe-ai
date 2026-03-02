# backend/src/services/rag/chunking/chunker.py : 삭제하면 안되는 파일.

import re
from typing import List, Optional

from src.services.rag.parser.schema import POI
from .schema import POIChunk


_SENT_SPLIT = re.compile(r"(?<=[.!?。！？])\s+|(?<=\.)\s+|(?<=\?)\s+|(?<=!)\s+")
_KR_SENT_SPLIT = re.compile(r"(?<=[다요죠임함]\.)\s+|(?<=[다요죠임함]\s)\s+")  # 느슨한 보조


class JungguChunker:
    """
    POI -> 검색용 청크로 변환.
    - mode="poi": POI 1개 = 청크 1개
    - mode="sentence": POI 내부 문장 단위로 청크 생성 (정밀 검색용)
    - mode="window": 문장 n개씩 슬라이딩 윈도우(연속 문맥 강화)
    """

    def __init__(
        self,
        mode: str = "sentence",
        window_size: int = 3,
        window_stride: int = 1,
        min_chars: int = 40,
    ):
        self.mode = mode
        self.window_size = window_size
        self.window_stride = window_stride
        self.min_chars = min_chars

    def build(self, pois: List[POI]) -> List[POIChunk]:
        chunks: List[POIChunk] = []

        for i, poi in enumerate(pois):
            if self.mode == "poi":
                chunk = self._chunk_from_poi(i, poi)
                if chunk:
                    chunks.append(chunk)

            elif self.mode == "sentence":
                chunks.extend(self._chunks_by_sentence(i, poi))

            elif self.mode == "window":
                chunks.extend(self._chunks_by_sentence_window(i, poi))

            else:
                raise ValueError(f"Unsupported mode: {self.mode}")

        return chunks

    def _poi_context_text(self, poi: POI) -> str:
        # 검색 품질 위해 meta성 텍스트를 본문에도 살짝 섞어줌(키워드 검색에도 유리)
        parts = [
            f"[카테고리] {poi.category}",
            f"[이름] {poi.name}",
        ]
        if poi.location:
            parts.append(f"[위치] {poi.location}")
        if poi.menu:
            parts.append(f"[메뉴] {poi.menu}")
        if poi.phone:
            parts.append(f"[연락처] {poi.phone}")
        if poi.tags:
            parts.append(f"[태그] {' '.join(poi.tags)}")
        if poi.description:
            parts.append(poi.description.strip())

        return "\n".join(parts).strip()

    def _chunk_from_poi(self, idx: int, poi: POI) -> Optional[POIChunk]:
        text = self._poi_context_text(poi)
        if len(text) < self.min_chars:
            return None

        return POIChunk(
            chunk_id=f"poi-{idx}",
            text=text,
            meta={
                "category": poi.category,
                "name": poi.name,
            },
        )

    def _split_sentences(self, text: str) -> List[str]:
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            return []
        # 1차: 일반 split
        sents = [s.strip() for s in _SENT_SPLIT.split(text) if s.strip()]
        # 너무 뭉개지면 한국어 보조 split 시도
        if len(sents) <= 1:
            sents = [s.strip() for s in _KR_SENT_SPLIT.split(text) if s.strip()]
        return sents

    def _chunks_by_sentence(self, idx: int, poi: POI) -> List[POIChunk]:
        base_meta = {"category": poi.category, "name": poi.name}
        desc = (poi.description or "").strip()
        if not desc:
            # 설명이 없으면 POI 통짜 청크로라도 하나 생성
            one = self._chunk_from_poi(idx, poi)
            return [one] if one else []

        sents = self._split_sentences(desc)
        chunks: List[POIChunk] = []

        for j, sent in enumerate(sents):
            sent = sent.strip()
            if len(sent) < self.min_chars:
                continue

            text = "\n".join(
                [
                    f"[카테고리] {poi.category}",
                    f"[이름] {poi.name}",
                    f"[문장] {sent}",
                    f"[위치] {poi.location}" if poi.location else "",
                ]
            ).strip()

            chunks.append(
                POIChunk(
                    chunk_id=f"poi-{idx}-sent-{j}",
                    text=text,
                    meta={**base_meta, "unit": "sentence", "sent_index": str(j)},
                )
            )

        # 문장이 너무 짧아서 다 걸러졌으면 fallback
        if not chunks:
            one = self._chunk_from_poi(idx, poi)
            return [one] if one else []

        return chunks

    def _chunks_by_sentence_window(self, idx: int, poi: POI) -> List[POIChunk]:
        base_meta = {"category": poi.category, "name": poi.name}
        desc = (poi.description or "").strip()
        if not desc:
            one = self._chunk_from_poi(idx, poi)
            return [one] if one else []

        sents = [s for s in self._split_sentences(desc) if s.strip()]
        if not sents:
            one = self._chunk_from_poi(idx, poi)
            return [one] if one else []

        chunks: List[POIChunk] = []
        w = self.window_size
        st = self.window_stride

        for start in range(0, max(1, len(sents) - w + 1), st):
            window = " ".join(sents[start : start + w]).strip()
            if len(window) < self.min_chars:
                continue

            text = "\n".join(
                [
                    f"[카테고리] {poi.category}",
                    f"[이름] {poi.name}",
                    f"[본문] {window}",
                    f"[위치] {poi.location}" if poi.location else "",
                ]
            ).strip()

            chunks.append(
                POIChunk(
                    chunk_id=f"poi-{idx}-win-{start}",
                    text=text,
                    meta={**base_meta, "unit": "window", "start": str(start), "size": str(w)},
                )
            )

        if not chunks:
            one = self._chunk_from_poi(idx, poi)
            return [one] if one else []
        return chunks