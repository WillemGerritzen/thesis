#!/bin/bash

set -e

cd "${HOME}"/job_logs

rm -r ../thesis/results
rm -r ../thesis/img/temp

#sed -i 's/# pool.apply_async(ppa.run_ppa())/pool.apply_async(ppa.run_ppa())/' "${HOME}"/thesis/main.py
#
#sbatch job
#
#sed -i 's/pool.apply_async(ppa.run_ppa())/# pool.apply_async(ppa.run_ppa())/' "${HOME}"/thesis/main.py
sed -i 's/# pool.apply_async(hc.run_hc())/pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py

sbatch job

sed -i 's/pool.apply_async(hc.run_hc())/# pool.apply_async(hc.run_hc())/' "${HOME}"/thesis/main.py
sed -i 's/# pool.apply_async(sa.run_sa())/pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py

sbatch job

sed -i 's/pool.apply_async(sa.run_sa())/# pool.apply_async(sa.run_sa())/' "${HOME}"/thesis/main.py

