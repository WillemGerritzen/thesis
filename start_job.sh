#!/bin/bash

set -e

DUMP_DIR="${HOME}"/Documents/Github/thesis/dump

echo "Moving into job_logs directory"
cd "${HOME}"/job_logs

for algo in "ppa"; do
  for run in {1..5}; do
    for image in "mondriaan" "starry_night" "mona_lisa" "the_kiss" "bach" "the_persistence_of_memory" "convergence"; do
      echo "Starting run ${run} for algorithm ${algo} on ${image}"
      name="${run}"_"${algo}"_"${image}"
      sbatch -J $name job "$algo" "$run" "$image"
    done
  done
done

exit 0