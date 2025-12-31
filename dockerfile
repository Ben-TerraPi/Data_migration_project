FROM python:3.12-slim

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source dans le conteneur
COPY src/ ./src/

# Créer le dossier dataset (sera rempli par le script)
RUN mkdir -p dataset

# Créer le dossier logs (pour éviter les erreurs d'accès)
RUN mkdir -p logs

# Définir la commande de lancement
CMD ["python", "src/main.py"]