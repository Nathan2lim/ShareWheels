#!/bin/bash
# Script pour remplacer les espaces par des underscores dans les noms de fichiers statiques

echo "Remplacement des espaces par des underscores dans les noms de fichiers statiques..."

# Fonction pour remplacer les espaces dans les noms de fichiers d'un dossier
replace_spaces() {
    find "$1" -type f -name "* *" | while read file; do
        # Le nom du fichier avec des underscores au lieu des espaces
        new_file=$(echo "$file" | sed 's/ /_/g')
        # Renommer le fichier
        mv "$file" "$new_file"
        echo "Renommé: $file -> $new_file"
    done
}

# Remplacer les espaces dans app/static
replace_spaces "/Users/nathangilbert/Desktop/Ynov/ShareWheels/app/static"

# Remplacer les espaces dans applicompte/static
replace_spaces "/Users/nathangilbert/Desktop/Ynov/ShareWheels/applicompte/static"

# Remplacer les espaces dans carte/static
replace_spaces "/Users/nathangilbert/Desktop/Ynov/ShareWheels/carte/static"

echo "Terminé!"
