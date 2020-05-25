from .celery import app
import requests
from .settings import CHAT_ID, BOT_TOKEN


@app.task
def send_message_order(text):
    params = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(BOT_TOKEN + 'sendMessage', data=params)
    return response

