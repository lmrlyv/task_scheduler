from os import environ

from celery import Celery


# Set the default Django settings module for the 'celery' program.
environ.setdefault("DJANGO_SETTINGS_MODULE", "task_scheduler.settings")

app = Celery("task_scheduler")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
