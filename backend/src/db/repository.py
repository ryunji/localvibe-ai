# db/repository.py
from src.db.database import SessionLocal
from src.db.models import Poi, PoiPeriod


def save_pois(pois: list[dict]):
    db = SessionLocal()

    try:
        for data in pois:
            poi = Poi(**data["poi"])
            db.add(poi)
            db.flush()

            period = data.get("period")
            if period:
                db.add(
                    PoiPeriod(
                        poi_id=poi.id,
                        **period
                    )
                )

        db.commit()

    except Exception as e:
        db.rollback()
        raise e

    finally:
        db.close()
