# Generated by Django 2.2.1 on 2021-08-17 07:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tabs', '0008_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='notes',
            name='person',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='notes', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
