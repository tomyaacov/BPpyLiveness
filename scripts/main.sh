#!/bin/bash

sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode r

sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode r --reward_mode r
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode r --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode r --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode r --reward_mode r

sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode ar --reward_mode r
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode ar --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode ar --reward_mode r
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode ar --reward_mode r

sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode a --reward_mode a

sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode r --reward_mode a
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode r --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode r --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode r --reward_mode a

sbatch scripts/run_main_single.sh --n 10 --k 3 --m 1 --total_timesteps 2000000 --state_mode ar --reward_mode a
sbatch scripts/run_main_single.sh --n 10 --k 6 --m 1 --total_timesteps 2000000 --state_mode ar --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 3 --m 1 --total_timesteps 4000000 --state_mode ar --reward_mode a
sbatch scripts/run_main_single.sh --n 20 --k 6 --m 1 --total_timesteps 4000000 --state_mode ar --reward_mode a


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
