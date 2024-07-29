# Utiliser une image de base Python 3.12
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc pkg-config libmariadb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurer l'environnement virtuel
RUN python -m venv /venv
ENV PATH="/venv/bin:$PATH"

# Mettre à jour pip
RUN pip install --upgrade pip

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . /app/

# RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "art_by_mtr.wsgi:application"]

