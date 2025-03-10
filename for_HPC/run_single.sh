#! /bin/bash

# these are variables to be used in the job queueing by the HPC:
#$ -q shai.q@bhn1089
#$ -cwd
#$ -N single_run
#$ -o ./logs/
#$ -j y

# running the python script
LD_LIBRARY_PATH=/gpfs0/shai/projects/software/Python/Python-3.11/lib/:$LD_LIBRARY_PATH
/gpfs0/shai/projects/software/Python/Python-3.11/bin/python3.11 main.py $1 $2 $3 $4 $5
