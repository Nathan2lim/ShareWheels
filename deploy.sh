#!/usr/bin/env bash
set -e
cd /srv/ShareWheels
git pull
rm -rf /srv/ShareWheels/staticfiles

# Créer les migrations si nécessaire
docker compose exec web python manage.py makemigrations app
docker compose exec web python manage.py makemigrations carte

# Reconstruire et démarrer les conteneurs
docker compose up -d --build

# Appliquer les migrations
docker compose exec web python manage.py migrate --noinput

# Collecter les fichiers statiques
docker compose exec web python manage.py collectstatic --noinput

echo "✅ Déploiement terminé $(date)"
