#!/bin/bash
### sbatch config parameters must start with #SBATCH and must precede any other command. to ignore just add another # - like so ##SBATCH
#SBATCH --partition main ### specify partition name where to run a job
#SBATCH --time 7-00:00:00 ### limit the time of job running. Format: D-H:MM:SS
#SBATCH --job-name run_main_ttt ### name of the job. replace my_job with your desired job name
#SBATCH --output run_main_ttt.out ### output log for running job - %J is the job number variable
#SBATCH --mail-user=tomya@post.bgu.ac.il ### users email for sending job status notifications ñ replace with yours
#SBATCH --mail-type=FAIL ### conditions when to send the email. ALL,BEGIN,END,FAIL, REQUEU, NONE
#SBATCH --mem=64G ### total amount of RAM // 500
#SBATCH --cpus-per-task=6	# 6 cpus per task – use for multithreading, usually with --tasks=1
#SBATCH --ntasks=4
#SBATCH --gpus=1

### Start you code below ####

out_file_name="output/ttt_out"


module load anaconda ### load anaconda module
source activate BPpyLiveness ### activating Conda environment. Environment must be configured before running the job
cd ~/repos/BPpyLiveness/ || exit
/usr/bin/time -a -o $out_file_name -f "time:%E,memory:%M" ~/.conda/envs/BPpyLiveness/bin/python main_mask_ttt.py  > $out_file_name