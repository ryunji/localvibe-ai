# src/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 🔹 MySQL 접속 정보
DB_USER = "root"
DB_PASSWORD = "gnosis260209"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "localvibe"

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