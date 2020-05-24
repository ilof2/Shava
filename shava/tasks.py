from .celery import app
from os import environ
import requests


@app.task
def send_message_order(text):
    params = {'chat_id': environ.get('CHAT_ID'), 'text': text}
    response = requests.post(environ.get('TOKEN') + 'sendMessage', data=params)
    return response

