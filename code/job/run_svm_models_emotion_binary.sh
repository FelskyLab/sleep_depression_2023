#!/bin/bash
#SBATCH --job-name=svm_emotion_binary   # Job name
#SBATCH --mail-type=FAIL            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=mohamed.abdelhack@camh.ca   # Where to send mail	
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=8gb                   # Job Memory
#SBATCH --time=00:30:00             # Time limit hrs:min:sec
#SBATCH --output=./script_outputs/svm_emotion_binary.log    # Standard output and error log

source ~/viz/bin/activate

INPUTS=($(<subjects_remaining_hcp_emotion_binary_svm_subjects_220716.txt))
#echo ${INPUTS[1]}
#my function
func () {
    f=$1
    python svm_all_subjects.py emotion_binary $f
}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
