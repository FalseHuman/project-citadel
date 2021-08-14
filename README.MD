# Project Citadel

## Setting up the installation

## Django
```bash
$ cd backend/citadel
$ pip install -r ./requirements.txt
```
### open settings.py and change the database to your own
```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'citadel', #change
        'USER': 'postgres', #change
        'PASSWORD': '12345', #change
    }
}
```
### launch Django
```bash
$ python manage.py migrate
$ python manage.py runserver 8002
```

## Vue
```bash
$ cd frontend
$ npm install
$ npm run serve
```

## DBMS PostgreSQL
Link how to install for [Windows](https://www.youtube.com/watch?v=yYJ74Sc7nw8)
Link how to install for [Linux](https://losst.ru/ustanovka-postgresql-ubuntu-16-04)