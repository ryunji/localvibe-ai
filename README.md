# localvibe-ai

**Summary : AI-powered web service that collects and displays local exhibitions using FastAPI and React

전시 / 문화 행사 정보를 수집하고 제공하는 웹 기반 AI 프로젝트입니다.  
Python(FastAPI) 백엔드와 React(Vite) 프론트엔드로 구성된 단일 저장소(monorepo) 구조를 사용합니다.

---

## 🖥️ Demo

(2026-01-13 기준)
> React UI에서 전시 수집 버튼을 클릭하면  
> FastAPI 백엔드의 AI 수집 로직이 실행되고  
> 결과가 실시간으로 화면에 렌더링됩니다.

---

## 📁 프로젝트 구조 (2026-01-13 기준)

    LOCALVIBE-AI/
    ├─ backend/         # ← 1) 서버 코드 영역(FastAPI + AI 수집 로직)
    ├─ frontend/        # ← 2) 클라이언트 코드 영역(React (Vite))
    ├─ localvibe-venv/  # ← 3) 로컬 개발 도구(Python 가상환경)
    ├─ .env             # ← 4) 환경 변수 파일(비밀 값, Git에 포함되지 않음)
    ├─ .gitignore       # ← 5) Git 관리 설정 파일
    └─ README.md        # ← 6) 프로젝트 설명 문서

> 참고  
> `venv`, `.env`, `.gitignore`는 서버 코드의 일부가 아닌  
> **프로젝트 전체 개발 환경의 구성 요소**이므로  
> 프로젝트 루트에 두는 것이 정석입니다.  
>  
> `localvibe-venv`는  
> “이 프로젝트는 Python이 주력이지만 backend 폴더에 종속되지 않는다”는 의미를 가집니다.

### 🔮 Possible Future Structure

    LOCALVIBE-AI
    ├─ services
    │   └─ backend
    ├─ apps
    │   └─ frontend

---

## ⚙️ Frontend Setup (React)

```bash
cd frontend
npm install
npm run dev
```

## ⚙️ Backend Setup (Python)

```bash
# 1) 가상환경 생성
python -m venv localvibe-venv

# 2.1) 가상환경 활성화 (Windows)
localvibe-venv\Scripts\activate

# 2.2) 가상환경 활성화 (Mac / Linux)
source localvibe-venv/bin/activate

# 3) 의존성 설치
pip install -r requirements.txt
```

---

## ✨ Development Goals

### Version 1
이 프로젝트는 단순한 API 연동 예제가 아니라,  
**콘솔 기반 Python AI 로직을 실제 웹 서비스 구조로 확장하는 경험**을 목표로 시작되었습니다.

기존에는:
- Python 콘솔에서 직접 실행하는 데이터 수집 스크립트였지만

현재는:
- FastAPI를 통해 AI 수집 로직을 API로 제공하고
- React UI에서 사용자가 직접 수집을 트리거하며
- 수집 결과를 실시간으로 확인할 수 있는 웹 애플리케이션 구조로 발전했습니다.

이 과정을 통해 다음과 같은 학습과 설계 경험을 얻는 것을 목표로 합니다.

- 콘솔 프로그램과 웹 서비스의 실행 모델 차이 이해
- 프론트엔드와 백엔드 간 책임 분리
- AI/데이터 수집 로직의 재사용 가능한 구조 설계
- 실제 서비스 확장을 고려한 프로젝트 구조 구성
---

## 🚀 Current Features

- 서울시 Open API 기반 전시/문화 행사 데이터 수집
- 전시 관련 키워드 필터링
- FastAPI `/collect` API 제공
- React UI에서 수집 트리거 및 결과 표시

## 🛠️ Planned Features

- 수집 데이터 DB 저장
- 전시 일정 기반 추천 로직
- 지도 기반 시각화
- 사용자 관심사 기반 필터링