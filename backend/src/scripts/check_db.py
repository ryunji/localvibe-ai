from db.database import SessionLocal
from db.models import Poi, PoiPeriod

def main():
    db = SessionLocal()

    try:
        print("📊 POI 개수:", db.query(Poi).count())
        print("📊 POI_PERIOD 개수:", db.query(PoiPeriod).count())
        print("-" * 50)

        pois = db.query(Poi).limit(10).all()
        for p in pois:
            print(
                f"[POI] id={p.id}, "
                f"name={p.name}, "
                f"type={p.poi_type}, "
                f"lat={p.latitude}, lng={p.longitude}"
            )

    finally:
        db.close()

if __name__ == "__main__":
    main()
