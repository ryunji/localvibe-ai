from fastapi import APIRouter
from src.db.database import SessionLocal
from src.db.models import Poi
from src.services.collector_service import run_collector

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/exhibitions")
def get_exhibitions():
    db = SessionLocal()
    try:
        pois = db.query(Poi).all()

        return [
            {
                "title": p.name,              # 프론트는 title 기대
                "place_name": p.place_name,
                "start_date": None,           # 아직 없으니까 None
                "end_date": None,
                "created_at": None,
            }
            for p in pois
        ]
    finally:
        db.close()

@router.get("/status")
def get_collect_status():
    return {
        "last_run_time": None,
        "status": None,
        "saved_count": 0,
    }
    
@router.post("/collect/manual")
def manual_collect():
    result = run_collector()
    return {
        "success": True,
        "data": result
    }    
    
