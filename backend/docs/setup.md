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