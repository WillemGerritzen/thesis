#!/bin/bash

set -e

RESULTS_DIR="${HOME}"/thesis/results
IMG_DIR="${HOME}"/thesis/img/temp

echo "Moving into job_logs directory"
cd "${HOME}"/job_logs

echo "Removing slurm logs"
rm slurm-*

if [ -d "${RESULTS_DIR}" ]; then
    echo "Removing results directory"
    rm -rf "${RESULTS_DIR}"
fi

if [ -d "${IMG_DIR}" ]; then
    echo "Removing image directory"
    rm -rf "${IMG_DIR}"
fi

# Hillclimber
sed -i 's/#pool.apply_async(ppa.run_ppa())/pool.apply_async(ppa.run_ppa())/' "${HOME}"/thesis/main.py
sed -i 's/#pool.apply_async(sa.run_sa())/pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py

echo "Starting hillclimber job"
sbatch job

# Simulated Annealing
sed -i 's/pool.apply_async(sa.run_sa())/#pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py
sed -i 's/#pool.apply_async(hc.run_hc())/pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py

echo "Starting simulated annealing job"
sbatch job

# PPA
#sed -i 's/pool.apply_async(hc.run_hc())/#pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py
#sed -i 's/#pool.apply_async(sa.run_sa())/pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py

#echo "Starting PPA job"
#sbatch job

# Reset
sed -i 's/pool.apply_async(hc.run_hc())/#pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py
sed -i 's/pool.apply_async(ppa.run_ppa())/#pool.apply_async(ppa.run_ppa())/' "${HOME}"/thesis/main.py

echo "Reset complete"
exit 0