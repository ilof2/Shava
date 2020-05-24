import os

from celery import Celery

os.environ['DJANGO_SETTINGS_MODULE'] = 'shava.settings'
app = Celery("shava")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

