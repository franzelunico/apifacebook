#!/bin/bash
rm -rf gettoken/migrations/*
find . -name "*.pyc" -exec rm -vrf {} \;
rm -rf gettoken/migrations/*
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell
python manage.py makemigrations gettoken
python manage.py migrate gettoken
python manage.py runserver 127.0.0.1:8001
