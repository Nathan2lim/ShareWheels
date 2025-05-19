#!/usr/bin/env bash
set -e

echo "Réorganisation des fichiers statiques pour éviter les doublons..."

# Créer une structure de dossier pour éviter les collisions
mkdir -p app/static/app_unique/{css,js}
mkdir -p applicompte/static/applicompte_unique/{css,js}
mkdir -p carte/static/carte_unique/{css,js}

# Déplacer les fichiers CSS app
echo "Traitement des fichiers CSS de l'app..."
find app/static/app/css -type f -name "*.css" | while read file; do
    basename=$(basename "$file")
    cp "$file" "app/static/app_unique/css/$basename"
done

# Déplacer les fichiers JS app
echo "Traitement des fichiers JS de l'app..."
find app/static/app/js -type f -name "*.js" | while read file; do
    basename=$(basename "$file")
    cp "$file" "app/static/app_unique/js/$basename"
done

# Déplacer les fichiers CSS applicompte
echo "Traitement des fichiers CSS de applicompte..."
find applicompte/static/applicompte/css -type f -name "*.css" | while read file; do
    basename=$(basename "$file")
    cp "$file" "applicompte/static/applicompte_unique/css/$basename"
done

# Déplacer les fichiers JS applicompte
echo "Traitement des fichiers JS de applicompte..."
find applicompte/static/applicompte/js -type f -name "*.js" | while read file; do
    basename=$(basename "$file")
    cp "$file" "applicompte/static/applicompte_unique/js/$basename"
done

# Déplacer les fichiers CSS carte
echo "Traitement des fichiers CSS de carte..."
find carte/static/carte/css -type f -name "*.css" | while read file; do
    basename=$(basename "$file")
    cp "$file" "carte/static/carte_unique/css/$basename"
done

# Déplacer les fichiers JS carte
echo "Traitement des fichiers JS de carte..."
find carte/static/carte/js -type f -name "*.js" | while read file; do
    basename=$(basename "$file")
    cp "$file" "carte/static/carte_unique/js/$basename"
done

echo "✅ Réorganisation terminée !"
echo "Vous pouvez maintenant ajuster vos templates pour utiliser les nouveaux chemins."
echo "Exemple: {% static 'app_unique/css/nom_fichier.css' %} au lieu de {% static 'app/css/nom_fichier.css' %}"
