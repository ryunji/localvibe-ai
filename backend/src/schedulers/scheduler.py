from core.scheduler import BaseScheduler
from services.collector_service import collect_seoul_events

class SeoulEventScheduler(BaseScheduler):

    def register(self, scheduler):
        scheduler.add_job(
            collect_seoul_events,
            "cron",
            hour=3
        )
