# services/collector_service.py
from src.collectors.seoul_open_data_cultural_event import collect_seoul_pois

def run_collector():
    return collect_seoul_pois()
