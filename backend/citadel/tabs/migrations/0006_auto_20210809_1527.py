# Generated by Django 2.2.1 on 2021-08-09 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0005_auto_20210809_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pays',
            name='type_of_pays',
            field=models.CharField(choices=[('Карта', 'Карта'), ('Наличные', 'Наличные')], max_length=255, verbose_name='Тип платежа'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
