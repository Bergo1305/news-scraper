from .celerysettings import app as celery_app
from celery.schedules import crontab
from datetime import datetime
import news_scraper.tasks

__all__ = ('celery_app',)

celery_app.conf.beat_schedule = {
    "collect_data": {
        "task": "news_scraper.tasks.collect_data",
        "schedule": crontab(minute=1),
        "start_time": datetime.utcnow()
    }
}
celery_app.conf.timezone = 'UTC'
