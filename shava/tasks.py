from .celery import app


@app.task
def send_email():
    pass
