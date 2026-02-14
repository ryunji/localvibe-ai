# db/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) 프로젝트 루트(backend) 경로 계산
#    db/database.py -> db -> src -> backend
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

# 2) data/rdb 폴더 생성
RDB_DIR = os.path.join(BASE_DIR, "data", "rdb")
os.makedirs(RDB_DIR, exist_ok=True)

# 3) sqlite 파일 경로 확정
DB_PATH = os.path.join(RDB_DIR, "poi.db")

# 4) SQLAlchemy 접속 URL (윈도우 경로는 슬래시/역슬래시 이슈가 있으니 절대경로 권장)
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# 5) 엔진 생성 (여기가 실제로 DB에 연결하는 핵심)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 멀티스레드 관련 옵션(필요한 경우가 많음)
    echo=True,                                  # SQL 로그 출력
)

# 6) 세션 공장(=DB 작업용 연결을 찍어내는 공장)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# 7) ORM 모델들이 상속받을 Base
Base = declarative_base()

def init_db():
    """DB 파일 + 모든 테이블 생성"""
    print(f"📦 DB 초기화 시작 (테이블 생성) -> {DB_PATH}")
    Base.metadata.create_all(bind=engine)
    print("✅ DB 초기화 완료")
