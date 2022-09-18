from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.core.files.storage import default_storage
from django.db import models
from django.contrib.postgres.fields import JSONField

class User(AbstractUser):
    photo = models.ImageField(blank=True, null=True)
    email_send = models.BooleanField(default=False)

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

class TokenReset(models.Model):
    token_for_user = models.ForeignKey(
        User, related_name='token', on_delete=models.CASCADE)
    token = models.CharField(max_length=255, verbose_name="Token")

class Categories(models.Model):
    title = models.CharField(max_length=255, verbose_name="Нзвание категории")
    cost = models.DecimalField(default='0.00', blank=True, max_digits=30,
                               decimal_places=2, verbose_name='Лимит категории')

class Pays(models.Model):
    TYPE_PAYS = (
        ('карта', 'Карта'),
        ('наличные', 'Наличные')
    )
    MONTH = (
        ('Январь', 'Январь'),
        ('Февраль', 'Февраль'),
        ('Март', 'Март'),
        ('Апрель', 'Апрель'),
        ('Май', 'Май'),
        ('Июнь', 'Июнь'),
        ('Июль', 'Июль'),
        ('Август', 'Август'),
        ('Сентябрь', 'Сентябрь'),
        ('Октябрь', 'Октябрь'),
        ('Ноябрь', 'Ноябрь'),
        ('Декабрь', 'Декабрь'),
    )
    author = models.ForeignKey(
        User, related_name='pays', on_delete=models.CASCADE)
    categories = models.ForeignKey(
        Categories, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name="Назначение платежа")
    body = models.TextField(blank=True, null=True,
                            verbose_name="Описание платежа")
    cost = models.DecimalField(default='0.00', blank=True, max_digits=30,
                               decimal_places=2, verbose_name='Сумма списания/пополнения')

    data = models.DateTimeField(auto_now_add=True)
    type_of_pays = models.CharField(max_length=255,
                                    choices=TYPE_PAYS, verbose_name='Тип платежа')
    month = models.CharField(max_length=255,
                             choices=MONTH, verbose_name='Месяц')


class Notes(models.Model):
    person = models.ForeignKey(
        User, related_name='notes', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True,
                             null=True, verbose_name='Название')
    body = models.TextField(blank=True, null=True, verbose_name="Текст")


class Templates(models.Model):
    person = models.ForeignKey(
        User, related_name='templates', on_delete=models.CASCADE)
    body_template = JSONField(verbose_name="Тело шаблона")
