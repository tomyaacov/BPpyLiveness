#!/bin/bash

sbatch scripts/run_main_single.sh --n 5 --k 1 --m 1 --total_timesteps 1000 --state_mode a --reward_mode r --job-name run_main_a --output run_main_a.out
sbatch scripts/run_main_single.sh --n 6 --k 1 --m 1 --total_timesteps 1000 --state_mode a --reward_mode r --job-name run_main_b --output run_main_b.out
