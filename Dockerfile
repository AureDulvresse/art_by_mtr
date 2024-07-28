# Utiliser une image de base Python 3.12
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires
RUN apt update && \
    apt install -y --no-install-recommends gcc pkg-config libmariadb-dev && \
    apt clean && \
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
COPY . .

# Exposer le port que l'application utilisera
EXPOSE 8000

# Démarrer l'application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "art_by_mtr.wsgi:application"]
