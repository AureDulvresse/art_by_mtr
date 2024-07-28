# Utiliser une image de base Python 3.12
FROM python:3.12-slim

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

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . ./app

COPY ./entrypoint.sh /
ENTRYPOINT [ "sh", "/entrypoint.sh" ]

# Exposer le port que l'application utilisera
EXPOSE 8000