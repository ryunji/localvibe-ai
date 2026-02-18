import os
import requests
from dotenv import load_dotenv

load_dotenv()

SEOUL_API_URL = "http://openapi.seoul.go.kr:8088"
API_KEY = os.getenv("SEOUL_API_KEY")

def fetch_seoul_events(limit: int = 1000) -> list[dict]:
    if not API_KEY:
        raise RuntimeError("SEOUL_API_KEY 환경변수가 설정되지 않았습니다")

    url = f"{SEOUL_API_URL}/{API_KEY}/json/culturalEventInfo/1/{limit}"
    res = requests.get(url, timeout=10)
    res.raise_for_status()

    data = res.json()
    return data.get("culturalEventInfo", {}).get("row", [])
