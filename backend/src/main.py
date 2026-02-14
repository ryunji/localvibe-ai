"""
LocalVibe-AI - FastAPI Entry Point

이 파일은 오직 서버 '조립'만 담당한다.
- 앱(app) 생성
- 라우터 등록
- 미들웨어 등록
- lifespan 연결
"""

# ===========================================================================
# 1. 표준 라이브러리 import
# ===========================================================================
import runpy
import os

# ===========================================================================
# 2. FastAPI 관련 라이브러리 import
# ===========================================================================
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

# ===========================================================================
# 3. 내부 모듈 import
# ===========================================================================
from src.routes.chat import router as chat_router
from src.db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("서버 시작...!")
    yield                   # ← 여기서 서버가 실제로 동작 시작
    print("서버 종료...")

##############################################################################
# 2. 서버 시작/종료 관리 (lifespan)
##############################################################################
app = FastAPI(lifespan=lifespan)

app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from src.db.database import SessionLocal

@app.get("/health")
def health():
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        return {
            "status": "ok",
            "database": "connected"
        }
    except Exception as e:
        return {
            "status": "error",
            "database": "failed",
            "detail": str(e)
        }
    finally:
        db.close()    
        
@app.get("/")
def root():
    return {
      "service" : "LocalVibe"
    , "status"  : "running"
    , "version" : "1.0.0"
}

##############################################################################
# FastAPI/uvicorn 구조로 전환하기 전,
# 디버그 단독 실행 테스트용으로 사용하던 main 함수 (현재는 사용하지 않음)
##############################################################################
def main():
    
    # 파이썬은 줄바꿈 자체가 문장의 끝이므로, 써도 무방하지만 세미콜론(;)을 쓰지 않는다.
    runpy.run_path("src/collectors/seoul_api.py", run_name="__main__")

# Python은 모든 파일에 자동으로 __name__ 변수를 만든다.
# 코드의 의미 → 이 파일이 직접 실행될 때만 아래 코드 실행해라
# 직접 실행이라 함은 ex) python main.py

# 자동으로 name에 변수가 main으로 들어간다..?
# import 할때는 main이 아니게 되고, 그 경우에는 : 다음의 코드를 실행하지 않음.
if __name__ == "__main__":
    mode = os.getenv("APP_MODE", "server")

    if mode == "server":
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000) # 맨 마지막 인자는 reload로 reload=False인 상태.
    elif mode == "debug":
        main()
