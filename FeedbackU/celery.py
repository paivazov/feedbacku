import os

from django import setup as django_setup

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FeedbackU.settings')
django_setup()

app = Celery('FeedbackU')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



