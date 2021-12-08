import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'secret_notes.settings')

app = Celery('secret_notes')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'purge-notes': {
        'task': 'notes.tasks.purge_notes',
        'schedule': crontab()
    },
}

app.autodiscover_tasks()
