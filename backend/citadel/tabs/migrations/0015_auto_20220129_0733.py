# Generated by Django 2.2.1 on 2022-01-29 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0014_token'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Token',
            new_name='TokenReset',
        ),
    ]
