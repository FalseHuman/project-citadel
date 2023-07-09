from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from tabs.models import Pays, User, Notes
from core.settings import DATE_FORMAT
import pytz


class Command(BaseCommand):
    help = 'fix time'

    def handle(self, *args, **kwargs):
        pays = Pays.objects.all()
        print('Start convert to Europe/Moscow')
        for pay in pays:
            pay.data = pay.data.astimezone(pytz.timezone('Europe/Moscow'))
            pay.save()
        print('End convert to Europe/Moscow')