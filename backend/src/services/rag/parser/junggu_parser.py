# backend/src/services/rag/parser/junggu_parser.py

import re
from pathlib import Path
from typing import List
from .schema import POI


class JungguPDFParser:
    """
    중구 시리즈 PDF 텍스트를 구조화하는 파서
    """

    CATEGORY_KEYWORDS = [
        "FOOD & DRINK",
        "SHOP & SPACE",
        "ART & CULTURE",
        "HERITAGE",
    ]

    def __init__(self):
        pass

    def parse(self, text: str) -> List[POI]:
        """
        전체 텍스트를 POI 단위로 분리
        """

        lines = [line.strip() for line in text.split("\n") if line.strip()]
        pois = []

        current_category = None
        buffer = []

        for line in lines:

            # 카테고리 감지
            if any(keyword in line for keyword in self.CATEGORY_KEYWORDS):
                current_category = line
                continue

            buffer.append(line)

        # 🔥 여기서 장소 단위 분리 로직 추가 필요
        pois = self._split_poi_blocks(buffer, current_category)

        return pois

    def _split_poi_blocks(self, lines: List[str], category: str) -> List[POI]:
        """
        장소 단위 블록 분리
        """

        blocks = []
        current_block = []

        for line in lines:
            # 간단한 heuristic:
            # 장소명은 보통 짧고 특수문자 없음
            if len(line) < 20 and not line.startswith("#") and current_block:
                blocks.append(current_block)
                current_block = []

            current_block.append(line)

        if current_block:
            blocks.append(current_block)

        pois = []

        for block in blocks:
            poi = self._build_poi(block, category)
            if poi:
                pois.append(poi)

        return pois

    def _build_poi(self, block: List[str], category: str) -> POI:
        """
        블록을 POI 객체로 변환
        """

        name = block[0]
        description = ""
        menu = None
        location = None
        phone = None
        tags = []

        for line in block[1:]:

            if line.startswith("#"):
                tags.extend(line.replace("#", "").split())

            elif "대표메뉴" in line:
                menu = line

            elif "위치" in line:
                location = line

            elif "연락처" in line:
                phone = line

            else:
                description += line + " "

        return POI(
            category=category,
            name=name,
            description=description.strip(),
            menu=menu,
            location=location,
            phone=phone,
            tags=tags,
        )