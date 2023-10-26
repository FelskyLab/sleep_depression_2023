#!/bin/bash
#SBATCH --job-name=seed_based_correlation   # Job name
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=8gb                   # Job Memory
#SBATCH --time=02:30:00             # Time limit hrs:min:sec
#SBATCH --output=./LOG_seed_based_corr_hcp180.log    # Standard output and error log

module load bio/FSL/6.0.5.1-centos7_64

INPUTS=($(<../../data/subject_list.txt))
func () {
    f=$1
    echo $f
    mkdir ../../data/resting/processed/seed_based_correlation/"$f"/
    while read roi ; do
      echo $roi
      dual_regression ../../data/resting/roi/"$f"/"$roi".nii.gz 0 -1 0 \
      ../../data/resting/processed/seed_based_correlation/"$f"/"${roi//-/_}"\
      ../../data/resting/activation/"$f"_20227_2_0/fMRI/rfMRI.ica/filtered_func_data_clean.nii.gz
    done < ../../data/roi_names.txt
}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"

