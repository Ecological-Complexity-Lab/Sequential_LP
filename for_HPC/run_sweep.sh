#! /bin/bash

# these are variables to be used in the job queueing by the HPC:
#$ -q shai.q@bhn27
#$ -cwd
#$ -N single_sweep   
#$ -l h_vmem=2G
#$ -j y

# running the python script
LD_LIBRARY_PATH=/gpfs0/shai/projects/software/Python/Python-3.11/lib/:$LD_LIBRARY_PATH
/gpfs0/shai/projects/software/Python/Python-3.11/bin/python3 main_sweep.py $1 $2 $3
