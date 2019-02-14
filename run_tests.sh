#!/usr/bin/env bash
echo 'Running tests...'
python manage.py migrate
python manage.py test
