# Utiliser une image de base Python 3.12
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires
RUN apt update && \
    apt install -y --no-install-recommends gcc pkg-config mysql-client libmariadb-dev && \
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

# Copier le script d'entrypoint
COPY entrypoint.sh /entrypoint.sh

# Rendre le script exécutable
RUN chmod +x /entrypoint.sh

# Exposer le port que l'application utilisera
EXPOSE 8000

# Définir le script d'entrypoint
ENTRYPOINT ["/entrypoint.sh"]
