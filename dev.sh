#!/bin/bash

# Arrêter tous les conteneurs existants
docker-compose down

# Démarrer les conteneurs avec la configuration de développement
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# Afficher les conteneurs en cours d'exécution
docker ps

echo "Environnement de développement démarré. Accédez à l'application sur http://localhost:8000"
