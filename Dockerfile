FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers nécessaires
COPY . /app

# Copier le script wait-for-it.sh
COPY wait-for-it.sh /app/wait-for-it.sh

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Rendre le script exécutable
RUN chmod +x /app/wait-for-it.sh

CMD ["./wait-for-it.sh", "mysql:3306", "--", "python", "main.py"]