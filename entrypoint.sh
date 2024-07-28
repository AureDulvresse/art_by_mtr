#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn art_by_mtr.wsgi:application --bind 0.0.0.0:8000
