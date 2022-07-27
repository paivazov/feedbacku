import os

# idk if this django.setup is being needed. Re-run project on new machine
# If celery raises error - try to enable django_setup
from django import setup as django_setup  # noqa: F401

from celery.schedules import crontab
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FeedbackU.settings')
# django_setup()

app = Celery('FeedbackU')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'erase-old-invitations': {
        'task': 'organisations.tasks.erase_old_invitations',
        'schedule': crontab(0, 0, day_of_month='1'),
    },
}
