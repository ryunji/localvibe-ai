# src/collectors/seoul_api.py
import requests
import os

from src.db.repository import save_pois
from src.db.database import init_db
from dotenv import load_dotenv

load_dotenv()

SEOUL_API_URL = "http://openapi.seoul.go.kr:8088"
API_KEY = os.getenv("SEOUL_API_KEY")


def fetch_seoul_events():
    if not API_KEY:
        raise RuntimeError("❌ SEOUL_API_KEY 환경변수가 설정되지 않았습니다")

    url = f"{SEOUL_API_URL}/{API_KEY}/json/culturalEventInfo/1/1000"
    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    return data["culturalEventInfo"]["row"]


def collect_seoul_pois():
    raw_events = fetch_seoul_events()
    print(f"📡 서울 API 수신: {len(raw_events)}건")

    pois = []

    for idx, e in enumerate(raw_events, start=1):
        print(f"🔄 변환 중 [{idx}/{len(raw_events)}] {e.get('TITLE')}")

        poi_data = {
            "poi": {
                "name": e.get("TITLE"),
                "poi_type": e.get("CODENAME"),
                "source": "seoul_api",

                "place_name": e.get("PLACE"),
                "address": e.get("ADDR"),

                "latitude": float(e["LAT"]) if e.get("LAT") else None,
                "longitude": float(e["LOT"]) if e.get("LOT") else None,

                "use_fee": e.get("USE_FEE"),
                "target": e.get("USE_TRGT"),
                "contact": e.get("ORG_LINK"),
                "homepage": e.get("HOMEPAGE"),
            }
        }

        # 기간 정보 (있는 경우만)
        if e.get("STRTDATE") or e.get("END_DATE"):
            poi_data["period"] = {
                "start_date": e.get("STRTDATE"),
                "end_date": e.get("END_DATE"),
            }

        pois.append(poi_data)

    print(f"💾 DB 저장 시작: {len(pois)}건")
    save_pois(pois)
    print("🎉 수집 완료")


def main():
    print("📦 DB 초기화 시작")
    init_db()              # ✅ 반드시 먼저
    print("✅ DB 초기화 완료")

    collect_seoul_pois()   # ✅ 그 다음 수집


if __name__ == "__main__":
    main()
