# POI - 장소 마스터
from sqlalchemy import Column, Integer, String, Float, DECIMAL, Text, Index
from src.db.database import Base

class Poi(Base):
    __tablename__ = "poi"
    __table_args__ = (
        Index("idx_poi_type", "poi_type"),
        Index("idx_poi_location", "latitude", "longitude"),
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
        },
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    # 🔹 기본 정보
    name = Column(String(255), nullable=False)
    poi_type = Column(String(50))       # CULTURE / FESTIVAL / NATURE ...
    source = Column(String(50))         # SEOUL_API 등

    place_name = Column(String(255))
    address = Column(String(500))

    # 🔹 위치 정보 (Float ❌ → DECIMAL ⭕)
    latitude = Column(DECIMAL(10, 7), nullable=False)
    longitude = Column(DECIMAL(10, 7), nullable=False)

    # 🔹 부가 정보
    use_fee = Column(String(255))
    target = Column(String(255))
    contact = Column(Text)
    homepage = Column(Text)