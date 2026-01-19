# 이것은 한줄 주석, 코드 옆에도 사용이 가능하다.
"""
이것은 Docstring (문서화 문자열)
한줄 주석인 #과 달리 여러 줄 작성이 가능하다.
"""
##########################################################################
"""
LocalVibe AI - FastAPI 서버

1. 설치 필요 목록 :
   
   1.1. uvicorn     : pip install uvicorn fastapi 
   1.2. apscheduler : pip install apscheduler  
   
   * 참고사항 : requirements.txt에 
               ex) uvicorn==0.27.0
               와 같이 패키지를 추가한 후, 터미널(콘솔)에서 다음 명령어를 실행하여 설치할 수도 있다.
               pip install -r requirements.txt
               이 명령은 requirements.txt에 적힌 패키지 중
               이미 설치되어 있고 버전도 충족하면 그대로 사용(재설치 안 함)
               없거나 버전이 다르면 설치/업데이트/다운그레이드가 발생할 수 있다.
               참고로, requirements.txt에 없다고 해서 기존 설치 패키지가 삭제되지는 않는다.
              (삭제는 pip uninstall이나 새 가상환경 생성이 필요)

2. 실행방법 : 

  1) python main.py 
     → (현재 코드 기준으로) main.py 내부에서 uvicorn.run()을 호출하여 FastAPI를 실행한다.
       (명령어 python main.py는 FastAPI를 실행하는게 아니라,
       서버인 uvicorn 즉 uvicorn.run()을 직접 호출해서 실행하는 것, FastAPI 자체는 서버가 아님)
       reload=False(기본값)로 동작하며, 단일 프로세스로 실행된다.
       reload가 없어(코드를 수정해도 재시작되지 않는다, 아무 일 없음) 
       코드 변경 시 자동 재시작되지 않으므로 Ctrl+C 후 재실행이 필요하다.
       
  2) uvicorn main:app --reload
     → uvicorn으로 직접 실행한다.
       uvicorn은 ASGI 서버(FastAPI를 실행하는 웹 서버)로 Node.js의 node 명령어와 같다.
       main은 실행할 Python 파일명(main.py)을 의미하고, 
       app은 해당 파일에 정의된 FastAPI 인스턴스 변수(app)를 의미한다.
       --reload는 파일을 수정하면 자동으로 재시작하라는 의미이고, 개발할 때만 사용하고 프로덕션에서는 빼야한다.
       부모 프로세스(감시 담당) + 자식 프로세스(서버 담당)로 2개의 프로세스가 실행되고, 
       파일 감시 프로세스가 변경을 감지하여
       코드를 수정하면 자동으로 재시작한다. 개발할 때 편의를 위해 사용된다.
       
 * 요약 : uvicorn [파일명]:[FastAPI객체] [옵션] 형식
"""

from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler
from src.collectors.seoul_api import SeoulAPICollector
from datetime import datetime
import runpy
from fastapi.middleware.cors import CORSMiddleware
from src.routes.chat import router as chat_router

# 전역 스케줄러
scheduler = None


# 수집하는 메서드 호출한다.
def run_collector():
    """src/collectors/seoul_api.py 실행"""
    print(f"\n🚀 수집 시작 - {datetime.now()}")
    
    # 기존에 main으로 실행
    #runpy.run_path("src/collectors/seoul_api.py", run_name="__main__")
    # 26.01.12.월요일 추가 : 객체생성
    collector = SeoulAPICollector()  
    raw = collector.fetch_exhibitions(start=1, end=150)
    return [collector.parse_to_model_data(r) for r in raw]
    print(f"✅ 완료 - {datetime.now()}\n")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """서버 시작/종료 시 실행"""
    global scheduler
    
    # 서버 시작시
    print("🚀 서버 시작!")
    
    # 서버 시작 시 최초 1회 수집 실행 (의도된 동작)
    run_collector()
    
    # 스케줄러 시작 (매일 3시)
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.add_job(run_collector, 'cron', hour=3, minute=0)
    scheduler.start()
    print("⏰ 스케줄러 시작: 매일 03:00\n")
    
    yield
    
    # 서버 종료시
    scheduler.shutdown()
    print("👋 서버 종료")


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

@app.get("/")
def root():
    return {
        "message": "LocalVibe API",
        "endpoints": {
            "/collect": "수동 수집 트리거"
        }
    }


@app.post("/collect")
def collect_now(background_tasks: BackgroundTasks):
    """수동 수집 트리거"""
    #background_tasks.add_task(run_collector)
    #return {"message": "수집 시작!"}
    result = run_collector()
    return {
        "count": len(result),
        "data": result
    }


#############################################################################


# FastAPI/uvicorn 구조로 전환하기 전,
# 단독 실행 테스트용으로 사용하던 main 함수 (현재는 사용하지 않음)
def main():
    
    # 파이썬은 줄바꿈 자체가 문장의 끝이므로, 써도 무방하지만 세미콜론(;)을 쓰지 않는다.
    runpy.run_path("src/collectors/seoul_api.py", run_name="__main__")

# Python은 모든 파일에 자동으로 __name__ 변수를 만든다.
# 코드의 의미 → 이 파일이 직접 실행될 때만 아래 코드 실행해라
# 직접 실행이라 함은 ex) python main.py

# 자동으로 name에 변수가 main으로 들어간다..?
# import 할때는 main이 아니게 되고, 그 경우에는 : 다음의 코드를 실행하지 않음.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) # 맨 마지막 인자는 reload=False인 상태.
    
    # FastAPI 사용하지 않을 경우에 썼던 코드.
    # main() 