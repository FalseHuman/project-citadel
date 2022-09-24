#!/bin/bash
python manage.py makemigrations --noinput
python manage.py migrate --noinput
gunicorn --certfile=/etc/nginx/certs/ssl/crm.khazieff.crt --keyfile=/etc/nginx/certs/ssl/crm.khazieff.key core.wsgi:application --bind 0.0.0.0:443