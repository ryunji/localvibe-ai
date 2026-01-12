# ============================================================
# src/models/exhibition.py (PostgreSQL 모델)
# ============================================================
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Exhibition(Base):
    """PostgreSQL에 저장되는 원본 데이터"""
    __tablename__ = 'exhibitions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # 기본 정보
    title = Column(String(500), nullable=False, index=True)
    place = Column(String(300))
    address = Column(String(500))
    
    # 날짜
    start_date = Column(String(100))
    end_date = Column(String(100))
    
    # 상세 정보
    use_fee = Column(String(200))
    target = Column(String(200))
    contact = Column(String(200))
    homepage = Column(Text)
    description = Column(Text)
    category = Column(String(100), index=True)
    
    # 위치 정보
    latitude = Column(Float)
    longitude = Column(Float)
    
    # 메타 정보
    source = Column(String(50), default='seoul_api')
    raw_json = Column(Text)  # 원본 API 응답 JSON
    
    # AI 동기화 상태
    synced_to_vector_db = Column(Boolean, default=False)
    vector_db_id = Column(String(100), unique=True)  # ChromaDB ID
    
    # 타임스탬프
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Exhibition(id={self.id}, title='{self.title}', synced={self.synced_to_vector_db})>"