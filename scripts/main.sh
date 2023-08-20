#!/bin/bash

sbatch scripts/run_main_single.sh --n 5 --k 1 --m 1 --total_timesteps 1000 --state_mode a --reward_mode r
sbatch scripts/run_main_single.sh --n 6 --k 1 --m 1 --total_timesteps 1000 --state_mode a --reward_mode r
