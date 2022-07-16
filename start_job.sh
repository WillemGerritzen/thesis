#!/bin/bash

set -e

RESULTS_DIR="${HOME}"/thesis/results
IMG_DIR="${HOME}"/thesis/img/temp

echo "Moving into job_logs directory"
cd "${HOME}"/job_logs

if [ -d "${RESULTS_DIR}" ]; then
    echo "Removing results directory"
    rm -rf "${RESULTS_DIR}"
fi

if [ -d "${IMG_DIR}" ]; then
    echo "Removing image directory"
    rm -rf "${IMG_DIR}"
fi

for algo in "hc" "ppa" "sa"; do
  for run in {1..5}; do
    if compgen -G "slurm-[0-9]*-$algo-$run.out" > /dev/null; then
      echo "Removing slurm log for previous run of $algo"
      rm "slurm-[0-9]*-$algo-$run.out"
  fi
    echo "Starting run ${run} for algorithm ${algo}"
    sbatch job "$algo" "$run"
  done
done

exit 0