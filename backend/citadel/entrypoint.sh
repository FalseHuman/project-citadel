#!/bin/bash
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn --certfile=/etc/nginx/certs/ssl/certs/crm.khazieff.crt --keyfile=/etc/ssl/certs/crm.khazieff.key core.wsgi:application --bind 0.0.0.0:443