#!/bin/bash
set -e

# Attendre que la base de données soit prête
while ! nc -z db 3306; do
  echo "En attente que la base de données MySQL soit prête..."
  sleep 1
done

# Appliquer les migrations de la base de données
echo "Appliquer les migrations de la base de données"
python manage.py migrate

# Collecter les fichiers statiques
echo "Collecter les fichiers statiques"
python manage.py collectstatic --noinput

# Démarrer Gunicorn
echo "Démarrer Gunicorn"
exec gunicorn art_by_mtr.wsgi:application --bind 0.0.0.0:8000
