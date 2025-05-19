#!/bin/bash
# Script pour créer et appliquer les migrations dans l'environnement Docker

echo "=== Création et application des migrations ==="
echo "1. Création des migrations pour l'application 'app'..."
docker compose exec web python manage.py makemigrations app

echo "2. Création des migrations pour l'application 'carte'..."
docker compose exec web python manage.py makemigrations carte

echo "3. Application des migrations..."
docker compose exec web python manage.py migrate

echo "4. Nettoyage du dossier 'staticfiles'..."
rm -rf staticfiles

echo "5. Collecte des fichiers statiques..."
docker compose exec web python manage.py collectstatic --noinput

echo "=== Processus terminé ==="
