#!/bin/bash

set -e

DUMP_DIR="${HOME}"/Documents/Github/thesis/dump

echo "Moving into job_logs directory"
cd "${HOME}"/job_logs

if [ "$1" != "-r" ]; then
  if [ -d "${DUMP_DIR}" ]; then
    read -p "Dump directory already exists. Do you want to delete it? [y/N] " -r
    echo "Removing results directory"
    rm -rf "${DUMP_DIR}"
  fi
fi

for algo in "ppa"; do
  for run in {1..5}; do
    for image in "mondriaan" "starry_night" "mona_lisa" "the_kiss" "bach" "the_persistence_of_memory" "convergence"; do
      echo "Starting run ${run} for algorithm ${algo}"
      sbatch job -J "$(date +"T")_${run}_${algo}_${image}" "$algo" "$run" "$image"
    done
  done
done

exit 0