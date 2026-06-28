# Utiliser une image Python officielle légère

FROM python:3.11-slim
# Installer les dépendances système (dont CMake et les compilateurs)
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail

WORKDIR /app

# Copier et installer les dépendances Python
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code
COPY . .

# Exposer le port (Render utilise 10000 par défaut)
EXPOSE 10000

# Démarrer l'application avec Gunicorn
CMD ["python", "app.py"]