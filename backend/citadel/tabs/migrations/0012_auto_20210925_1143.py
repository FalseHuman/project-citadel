# Generated by Django 2.2.1 on 2021-09-25 11:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0011_templates'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templates',
            name='body_template',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Тело шаблона'),
        ),
    ]
