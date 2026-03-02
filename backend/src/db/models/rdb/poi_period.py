# src/models/poi_period.py
from sqlalchemy import Column, Integer, Date, ForeignKey, Index
from src.db.database import Base

class PoiPeriod(Base):
    __tablename__ = "poi_period"
    __table_args__ = (
        Index("idx_poi_period_poi_id", "poi_id"),
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
        },
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    poi_id = Column(Integer, ForeignKey("poi.id"), nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
