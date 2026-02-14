# create_tables.py
from src.db.database import engine
from src.db.models import Base

Base.metadata.create_all(bind=engine)
print("✅ 테이블 생성 완료")
