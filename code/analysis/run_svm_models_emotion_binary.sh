#!/bin/bash
#SBATCH --job-name=svm_emotion_binary   # Job name
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=8gb                   # Job Memory
#SBATCH --time=00:30:00             # Time limit hrs:min:sec
#SBATCH --output=./LOG_svm_emotion_binary.log    # Standard output and error log

source ~/viz/bin/activate

INPUTS=($(<../../data/subject_list.txt))
func () {
    f=$1
    python svm_all_subjects.py emotion_binary $f
}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
