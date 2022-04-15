
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import check_status

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_status, 'interval', minutes=1)
    scheduler.start()