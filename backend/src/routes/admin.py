# ============================================================
# routes/admin.py
# ============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.exhibition import Exhibition

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/status")
def get_status():
    return {
        "scheduler_running": False,
        "last_run": None,
        "last_status": "idle"
    }

@router.get("/exhibitions")
def get_exhibitions(db: Session = Depends(get_db)):

    # 🔹 poi 테이블 기준 조회
    exhibitions = (
        db.query(Exhibition)
        .order_by(Exhibition.id.desc())   # created_at 없음 → id 기준
        .limit(100)
        .all()
    )

    return [
        {
            "id": e.id,
            "title": e.name,           # name → title로 매핑
            "poi_type": e.poi_type,
            "place_name": e.place_name,
            "address": e.address,
            "latitude": float(e.latitude),
            "longitude": float(e.longitude),
            "use_fee": e.use_fee,
            "target": e.target,
            "contact": e.contact,
            "homepage": e.homepage,
            "source": e.source,
        }
        for e in exhibitions
    ]
