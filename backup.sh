#!/bin/bash

TEMP_DIR="${HOME}"/thesis/dump/temp/
BACKUP_DIR="${HOME}"/thesis/backup/

if [ ! -d "$BACKUP_DIR" ]; then
  mkdir "$BACKUP_DIR"
fi

for run in {1..5}; do
  for image in "mondriaan" "starry_night" "mona_lisa" "the_kiss" "bach" "the_persistence_of_memory" "convergence"; do
    name="${run}"_ppa_"${image}".pkl
    if [ -f "$TEMP_DIR"$name ]; then
      if [ ! -f "$BACKUP_DIR"$name ]; then
        echo Found $name and backing it up to "$BACKUP_DIR"
        cp "$TEMP_DIR"$name "$BACKUP_DIR"$name
      fi
    fi
  done
done
