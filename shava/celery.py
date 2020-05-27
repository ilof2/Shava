import os

from celery import Celery
from celery.schedules import crontab

os.environ['DJANGO_SETTINGS_MODULE'] = 'shava.settings'
app = Celery("shava")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_every_thirty_seconds': {
        'task': 'shava.tasks.send_message_order',
        'schedule': 10,
    },
    'delete_not_sended_orders': {
        'task': 'shava.tasks.delete_not_sended_orders',
        'schedule': crontab(day_of_week=(0, 3, 6), minute=37, hour=1)
    }
}

