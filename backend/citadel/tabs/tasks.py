from core.celery import app
from celery_once import QueueOnce, AlreadyQueued
from django.core.management import call_command


@app.task(base=QueueOnce)
def email_send():
    call_command('email_send')
