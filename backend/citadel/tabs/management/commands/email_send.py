from django.core.management.base import BaseCommand
from django.core.mail import send_mail, EmailMessage
from tabs.models import User, Pays
from core.settings import DATE_FORMAT
import datetime
from django.conf import settings
from django.http import HttpResponse
from io import BytesIO
from django.template.loader import render_to_string
import weasyprint


class Command(BaseCommand):
    help = 'Email-рассылка'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начат процесс рассылки...")
        self.stdout.write(str(settings.STATIC_ROOT)+'/css/pdf.css')
        data = datetime.date.today()
        # TODO: реализовать массовую рассылку
        try:
            email_send_user = User.objects.filter(email_send=True)
            for i in range(len(email_send_user)):
                subject = 'Доброго времени суток {}, ваши расходы/доходы за этот месяц:'.format(
                    email_send_user[i].username)
                message = "Выписка расходов/доходов за этот месяц"
                email=EmailMessage(subject,message,
                    'emilkhazioff@yandex.ru',
                [email_send_user[i].email])
                # Формирование PDF.
                user = User.objects.get(id=email_send_user[i].id)
                pays = Pays.objects.filter(author=email_send_user[i].id)
                pays_cost = []
                expense = []
                income = []
                total = 0
                for z in range(len(pays)):
                    if datetime.datetime.date(pays[z].data).month == data.month:
                        pays_cost.append(pays[z])
                for i in pays_cost:
                    if i.cost > 0:
                        income.append(i.cost)
                    else:
                        expense.append(i.cost)
                    total += i.cost
                html = render_to_string('orders/order/pdf.html', {
                            'user': user, 'data': data, 'pays': pays_cost, 'total': total, "income": sum(income), 'expense': sum(expense)})
                out = BytesIO()

                stylesheets=[weasyprint.CSS(str(settings.STATIC_ROOT) + '/css/pdf.css')]
                weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
                # Прикрепляем PDF к электронному сообщению.
                email.attach('Exract_for_{}.pdf'.format(user.username), out.getvalue(),'application/pdf')
                # Отправка сообщения.'''
                email.send()
                #arr = Pays.objects.filter(author=email_send_user[i].id)
                '''subject = 'Доброго времени суток {}, ваши расходы/доходы за этот месяц:'.format(
                    email_send_user[i].username)
                message = ""
                count = 0'''
                '''for z in range(len(arr)):
                    if datetime.datetime.date(arr[z].data).month == month:
                        count += 1
                        message += str(count) + '. ' + "Назначение платежа: " + str(arr[z].title) + "\n" + "    Описание платежа: " + str(arr[z].body) + "\n" + "    Сумма списания/пополнения: " + str(
                            arr[z].cost) + " руб." + "\n" + "    Дата платежа: " + str(arr[z].data.strftime(DATE_FORMAT)) + "\n" "    Тип платежа: " + str(arr[z].type_of_pays).title() + "\n"

                if len(message) == 0:
                    message = "В этом месяце вы не вносили в систему расходы/доходы."

                send_mail(subject, message, 'emilkhazioff@yandex.ru',
                          [email_send_user[i].email])'''
            self.stdout.write("Сообщения отправлены.")
        except User.DoesNotExist:
            pass
