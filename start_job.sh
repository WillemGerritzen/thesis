#!/bin/bash

set -e

echo "Moving into job_logs directory"
cd "${HOME}"/job_logs

FFA=--ffa

for vertices in 20 100 300 500 700 1000; do
  for algo in "ppa" "hc" "sa"; do
    for run in {1..5}; do
      for image in "mondriaan" "starry_night" "mona_lisa" "the_kiss" "bach" "the_persistence_of_memory" "convergence"; do
        echo "Starting run ${run} for algorithm ${algo} on ${image} with ${vertices} vertices with FFA $FFA"
        name="${run}"_"${algo}"_"${image}"_"${vertices}"
        sbatch -J $name job.sh "$algo" "$run" "$image" "$vertices" "$FFA"
      done
    done
  done
done

exit 0