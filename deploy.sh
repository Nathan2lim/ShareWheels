#!/usr/bin/env bash
set -e
cd /srv/ShareWheels
echo "=== Début du déploiement ($(date)) ==="

echo "1. Récupération des dernières modifications..."
git pull

echo "2. Nettoyage du dossier 'staticfiles'..."
rm -rf /srv/ShareWheels/staticfiles

echo "3. Nettoyage du dossier 'images'..."
rm -rf /srv/ShareWheels/images

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

echo "3. Renommage des fichiers avec des espaces..."
# Remplacer les espaces dans les dossiers statiques
replace_spaces "/srv/ShareWheels/app/static"
replace_spaces "/srv/ShareWheels/applicompte/static"
replace_spaces "/srv/ShareWheels/carte/static"

echo "4. Création des migrations pour l'application 'app'..."
docker compose exec web python manage.py makemigrations app

echo "5. Création des migrations pour l'application 'carte'..."
docker compose exec web python manage.py makemigrations carte

echo "6. Reconstruire et démarrer les conteneurs..."
docker compose up -d --build

echo "7. Application des migrations..."
docker compose exec web python manage.py migrate --noinput

echo "8. Collecte des fichiers statiques..."
docker compose exec web python manage.py collectstatic --noinput

echo "✅ Déploiement terminé $(date)"
