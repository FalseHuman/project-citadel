import os

from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery("core")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.ONCE = {
    'backend': 'celery_once.backends.Redis',
    'settings': {
        'url': os.environ.get('CELERY_BROKER', 'redis://redis:6379/0'),
        'default_timeout': 60 * 60
    }
}
