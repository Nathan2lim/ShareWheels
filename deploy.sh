#!/usr/bin/env bash
set -e
cd /srv/ShareWheels
git pull
docker compose up -d --build
docker compose exec web python manage.py migrate --noinput
docker compose exec web python manage.py collectstatic --noinput
echo "✅ Déploiement terminé $(date)"
