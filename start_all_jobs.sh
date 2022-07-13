#!/bin/bash

set -e

RESULTS_DIR="${HOME}"/thesis/results
IMG_DIR="${HOME}"/thesis/img/temp

cd "${HOME}"/job_logs

if [ -d "${RESULTS_DIR}" ]; then
    rm -rf "${RESULTS_DIR}"
fi

if [ -d "${IMG_DIR}" ]; then
    rm -rf "${IMG_DIR}"
fi

# Hillclimber
sed -i 's/#pool.apply_async(ppa.run_ppa())/pool.apply_async(ppa.run_ppa())/' "${HOME}"/thesis/main.py
sed -i 's/#pool.apply_async(sa.run_sa())/pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py

sbatch job

# Simulated Annealing
sed -i 's/pool.apply_async(sa.run_sa())/#pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py
sed -i 's/#pool.apply_async(hc.run_hc())/pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py

sbatch job

# PPA
#sed -i 's/pool.apply_async(hc.run_hc())/#pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py
#sed -i 's/#pool.apply_async(sa.run_sa())/pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py

sbatch job

# Reset
sed -i 's/pool.apply_async(hc.run_hc())/#pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py
sed -i 's/pool.apply_async(ppa.run_ppa())/#pool.apply_async(ppa.run_ppa())/' "${HOME}"/thesis/main.py

