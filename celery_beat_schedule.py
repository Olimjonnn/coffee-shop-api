from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'delete-unverified-users-every-day': {
        'task': 'celery_worker.task_delete_unverified_users',
        'schedule': crontab(hour=0, minute=0),
    },
}