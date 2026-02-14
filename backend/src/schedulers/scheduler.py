def start_scheduler():
    scheduler = BackgroundScheduler(...)
    scheduler.add_job(run_collector, 'cron', hour=3)
    scheduler.start()
    return scheduler