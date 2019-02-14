#!/usr/bin/env bash
echo 'Starting...'
python manage.py migrate
python manage.py import_products
python manage.py reset_root_password
python manage.py runserver 0.0.0.0:80
