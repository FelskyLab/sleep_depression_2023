#!/bin/bash
#SBATCH --job-name=rdsa   # Job name
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=10gb                   # Job Memory
#SBATCH --time=00:40:00             # Time limit hrs:min:sec
#SBATCH --output=./LOG_rdsa.log    # Standard output and error log

source ~/viz/bin/activate

INPUTS=($(<../../data/subject_list.txt))
#echo ${INPUTS[1]}
#my function
func () {
    f=$1
    python rdsa_all_subjects.py $f
}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
