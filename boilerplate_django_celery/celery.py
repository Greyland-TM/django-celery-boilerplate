import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "boilerplate_django_celery.settings")

app = Celery( "boilerplate_django_celery")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Celery Beat Schedule
app.conf.beat_schedule = {
    'check-for-packages': {
        'task': 'apps.task_manager.tasks.daily_task_check',
        'schedule': crontab(minute='*/1'),
        'args': (),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
