# ============================================================
# src/models/exhibition.py  (MySQL - POI 테이블 모델)
# ============================================================

from sqlalchemy import Column, Integer, String, DECIMAL
from src.db.database import Base


class Exhibition(Base):
    """
    MySQL poi 테이블과 매핑되는 ORM 모델
    """

    __tablename__ = "poi"

    # 🔹 기본 키
    id = Column(Integer, primary_key=True, autoincrement=True)

    # 🔹 기본 정보
    name = Column(String(255), nullable=False)
    poi_type = Column(String(50))
    source = Column(String(50))
    place_name = Column(String(255))
    address = Column(String(500))

    # 🔹 위치 정보
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)

    # 🔹 추가 정보
    use_fee = Column(String(255))
    target = Column(String(255))
    contact = Column(String)
    homepage = Column(String)

    def __repr__(self):
        return f"<POI(id={self.id}, name='{self.name}', type='{self.poi_type}')>"
