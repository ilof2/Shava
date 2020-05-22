from celery import Celery


app = Celery("shava")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

