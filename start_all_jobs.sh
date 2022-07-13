#!/bin/bash

set -e

RESULTS_DIR="${HOME}"/thesis/results
IMG_DIR="${HOME}"/thesis/img/temp

echo "Moving into job_logs directory"
cd "${HOME}"/job_logs

if compgen -G "slurm-[0-9]*.out" > /dev/null; then
    echo "Removing slurm logs"
    rm slurm-*
fi

if [ -d "${RESULTS_DIR}" ]; then
    echo "Removing results directory"
    rm -rf "${RESULTS_DIR}"
fi

if [ -d "${IMG_DIR}" ]; then
    echo "Removing image directory"
    rm -rf "${IMG_DIR}"
fi

for algo in "hc" "ppa" "sa"; do
    sbatch job $algo
done

exit 0