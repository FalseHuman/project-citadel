from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from tabs.models import Pays, User, Notes
from core.settings import DATE_FORMAT
import datetime


class Command(BaseCommand):
    help = 'Email-рассылка'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начат процесс рассылки...")
        user = User.objects.get(username='Emil')
        for i in range(1, 40):
            Notes.objects.create(person_id = user.id, title=f"test {str(i)}", body="Апрель")