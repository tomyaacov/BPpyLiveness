#!/bin/bash

sbatch scripts/run_main_single.sh --n 10 --k 1 --m 1 --total_timesteps 1000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 30 --k 1 --m 1 --total_timesteps 3000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 40 --k 1 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 50 --k 1 --m 1 --total_timesteps 5000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 60 --k 1 --m 1 --total_timesteps 6000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 70 --k 1 --m 1 --total_timesteps 7000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 80 --k 1 --m 1 --total_timesteps 8000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 90 --k 1 --m 1 --total_timesteps 9000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 100 --k 1 --m 1 --total_timesteps 10000000 --state_mode a --reward_mode r

sbatch scripts/run_main_single.sh --n 10 --k 1 --m 1 --total_timesteps 1000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 30 --k 1 --m 1 --total_timesteps 3000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 40 --k 1 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 50 --k 1 --m 1 --total_timesteps 5000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 60 --k 1 --m 1 --total_timesteps 6000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 70 --k 1 --m 1 --total_timesteps 7000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 80 --k 1 --m 1 --total_timesteps 8000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 90 --k 1 --m 1 --total_timesteps 9000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 100 --k 1 --m 1 --total_timesteps 10000000 --state_mode a --reward_mode a


sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode r

sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode a



sbatch scripts/run_main_single.sh --n 10 --k 1 --m 2 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 10 --k 1 --m 3 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 10 --k 1 --m 4 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 2 --total_timesteps 4000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 3 --total_timesteps 4000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 4 --total_timesteps 4000000 --state_mode a --reward_mode r

sbatch scripts/run_main_single.sh --n 10 --k 1 --m 2 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 10 --k 1 --m 3 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 10 --k 1 --m 4 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 2 --total_timesteps 4000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 3 --total_timesteps 4000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 1 --m 4 --total_timesteps 4000000 --state_mode a --reward_mode a


