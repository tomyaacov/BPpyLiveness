#!/bin/bash



sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2500000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 10 --k 1 --m 2 --total_timesteps 2500000 --state_mode a --reward_mode a
