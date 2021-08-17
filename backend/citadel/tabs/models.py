from datetime import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models
import time
from core.settings import DATE_FORMAT


class User(AbstractUser):
    photo = models.ImageField(blank=True, null=True)

    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username


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
    title = models.CharField(max_length=255, blank=True, null=True, verbose_name='Название')
    body = models.TextField(blank=True, null=True, verbose_name="Текст")