# Generated by Django 2.2.1 on 2022-01-29 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0015_auto_20220129_0733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pays',
            name='type_of_pays',
            field=models.CharField(choices=[('Карта', 'Карта'), ('Наличные', 'Наличные')], max_length=255, verbose_name='Тип платежа'),
        ),
    ]
