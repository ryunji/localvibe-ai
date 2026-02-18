# src/db/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔹 .env 로드
load_dotenv()

# 🔹 MySQL 접속 정보
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# 🔹 SQLAlchemy MySQL 접속 URL
SQLALCHEMY_DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
)

# 🔹 엔진 생성
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,              # SQL 로그 출력
    pool_pre_ping=True,     # MySQL 연결 끊김 방지
)

# 🔹 세션 팩토리
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 🔹 ORM Base
Base = declarative_base()

def init_db():
    """MySQL 테이블 생성"""
    print("📦 DB 초기화 시작 (MySQL)")
    Base.metadata.create_all(bind=engine)
    print("✅ DB 초기화 완료")
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    