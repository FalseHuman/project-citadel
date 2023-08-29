from core.celery import app
from celery_once import QueueOnce, AlreadyQueued
from django.core.management import call_command
from django.core.mail import send_mail


@app.task(base=QueueOnce)
def email_send():
    call_command('email_send')


@app.task
def delay_send_email(
    subject: str,
    message: str,
    user_email: str,
    fail_silently: bool
    ):
    send_mail(
        subject,
        message,
        'emilkhazioff@yandex.ru',
        [f"{user_email}"],
        fail_silently,
    )
