#!/usr/bin/env bash
set -e

# Charge les variables du .env (attention si tu as des espaces ou des quotes)
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

if [ "${LOCAL}" = "1" ]; then
  echo "🛠 Environnement local (dev) détecté"
  docker-compose down
  docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
else

    cd /srv/ShareWheels
    echo "=== Début du déploiement ($(date)) ==="

    echo "1. Récupération des dernières modifications..."
    git pull

    echo "2. Nettoyage du dossier 'staticfiles'..."
    rm -rf /srv/ShareWheels/staticfiles

    echo "3. Nettoyage du dossier 'images'..."
    rm -rf /srv/ShareWheels/images

    echo "4. Nettoyage du dossier 'event_photos'..."
    rm -rf /srv/ShareWheels/event_photos

    # Fonction pour remplacer les espaces dans les noms de fichiers d'un dossier
    replace_spaces() {
        echo "Recherche de fichiers avec des espaces dans $1..."
        find "$1" -type f -name "* *" | while read file; do
            # Le nom du fichier avec des underscores au lieu des espaces
            new_file=$(echo "$file" | sed 's/ /_/g')
            # Renommer le fichier
            mv "$file" "$new_file"
            echo "Renommé: $file -> $new_file"
        done
    }

    echo "5. Renommage des fichiers avec des espaces..."
    # Remplacer les espaces dans les dossiers statiques
    replace_spaces "/srv/ShareWheels/app/static"
    replace_spaces "/srv/ShareWheels/applicompte/static"
    replace_spaces "/srv/ShareWheels/carte/static"

    echo "6. Création des migrations pour l'application 'app'..."
    docker compose exec web python manage.py makemigrations app

    echo "7. Création des migrations pour l'application 'carte'..."
    docker compose exec web python manage.py makemigrations carte

    echo "8. Reconstruire et démarrer les conteneurs..."
    docker compose down
    mkdir -p /srv/ShareWheels/staticfiles && chmod -R 777 /srv/ShareWheels/staticfiles
    docker compose up -d --build

    echo "9. Application des migrations..."
    docker compose exec web python manage.py migrate --noinput

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

    echo "✅ Déploiement terminé $(date)"
fi