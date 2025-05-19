#!/usr/bin/env bash
set -e

cd /srv/ShareWheels
echo "=== Début ddu deployement fichier static ==="

echo "10. Collecte des fichiers statiques..."
docker compose exec web bash -c "mkdir -p /app/staticfiles && chmod -R 777 /app/staticfiles"

# Création préalable des répertoires pour éviter l'erreur de fichiers statiques
docker compose exec web bash -c "
    for region in CAFR FR AR AZ BG CAES CN CZ DE DK EE ES ESMX FI GR HB HK HR HU ID IN IT JP KR LT LV MT MY NL NO PH PL PT PTBR RO RU SE SI SK TH TR TWTC UA US_UK VN; do
        mkdir -p /app/staticfiles/app/svg/ios/\$region/CMYK
        mkdir -p /app/staticfiles/app/svg/ios/\$region/RGB
    done
    
    for lang in fr it de ko th hr in zh-cn ja en pt-br sv no es; do
        mkdir -p /app/staticfiles/app/svg/android/\$lang
    done
    
    chmod -R 777 /app/staticfiles
"

docker compose exec web python manage.py collectstatic --noinput --clear
