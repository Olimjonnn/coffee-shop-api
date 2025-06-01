from celery import Celery
from app.core.config import settings
from celery_beat_schedule import CELERY_BEAT_SCHEDULE


celery_app = Celery(
    'worker',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

celery_app.conf.beat_schedule = CELERY_BEAT_SCHEDULE
celery_app.conf.timezone = 'UTC'

@celery_app.task
def task_delete_unverified_users():
    from app.tasks import delete_unverified_users
    result = delete_unverified_users()
    return result

celery_app.conf.task_routes = {
    'app.services.tasks.cleanup_unverified_users': {"queue": "default"}
}