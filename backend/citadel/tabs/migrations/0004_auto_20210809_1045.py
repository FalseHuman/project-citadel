# Generated by Django 2.2.1 on 2021-08-09 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0003_auto_20210720_1216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
