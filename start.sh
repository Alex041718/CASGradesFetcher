#!/bin/bash

# Vérifie si un paramètre est passé
if [ -z "$1" ]; then
  echo "Usage: $0 <arm64|x86>"
  exit 1
fi

# Sélectionne le fichier docker-compose en fonction du paramètre
if [ "$1" == "arm64" ]; then
  COMPOSE_FILE="docker-composeARM.yml"
elif [ "$1" == "x86" ]; then
  COMPOSE_FILE="docker-composeX86.yml"
else
  echo "Invalid parameter. Use 'arm64' or 'x86'."
  exit 1
fi

# Exécute les commandes Docker Compose avec le fichier sélectionné
docker compose -f $COMPOSE_FILE down
docker compose -f $COMPOSE_FILE up --build --detach