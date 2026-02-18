from src.collectors.seoul_open_data_cultural_event import fetch_seoul_events
from src.db.repository import save_pois

def _to_poi_payload(e: dict) -> dict:
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

    if e.get("STRTDATE") or e.get("END_DATE"):
        poi_data["period"] = {
            "start_date": e.get("STRTDATE"),
            "end_date": e.get("END_DATE"),
        }

    return poi_data


def run_collector(limit: int = 1000) -> dict:
    raw_events = fetch_seoul_events(limit=limit)
    pois = [_to_poi_payload(e) for e in raw_events]

    saved_count = save_pois(pois)  # save_pois가 저장 건수를 리턴하도록 바꾸는 걸 추천
    return {
        "received": len(raw_events),
        "to_save": len(pois),
        "saved": saved_count if saved_count is not None else len(pois),
    }
