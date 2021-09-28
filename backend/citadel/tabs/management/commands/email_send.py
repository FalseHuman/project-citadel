from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from tabs.models import User, Pays
from core.settings import DATE_FORMAT
import datetime


class Command(BaseCommand):
    help = 'Email-рассылка'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начат процесс рассылки...")
        month = datetime.date.today().month
        # TODO: реализовать массовую рассылку
        try:
            email_send_user = User.objects.filter(email_send=True)
            for i in range(len(email_send_user)):
                arr = Pays.objects.filter(author=email_send_user[i].id)

                subject = 'Доброго времени суток {}, ваши расходы/доходы за этот месяц:'.format(
                    email_send_user[i].username)
                message = ""
                count = 0
                for z in range(len(arr)):
                    if datetime.datetime.date(arr[z].data).month == month:
                        count += 1
                        message += str(count) + '. ' + "Назначение платежа: " + str(arr[z].title) + "\n" + "    Описание платежа: " + str(arr[z].body) + "\n" + "    Сумма списания/пополнения: " + str(
                            arr[z].cost) + " руб." + "\n" + "    Дата платежа: " + str(arr[z].data.strftime(DATE_FORMAT)) + "\n" "    Тип платежа: " + str(arr[z].type_of_pays).title() + "\n"

                if len(message) == 0:
                    message = "В этом месяце вы не вносили в систему расходы/доходы."

                send_mail(subject, message, 'emilkhazioff@yandex.ru',
                          [email_send_user[i].email])
            self.stdout.write("Сообщения отправлены.")
        except User.DoesNotExist:
            pass
