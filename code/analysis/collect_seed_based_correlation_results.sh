#!/bin/bash
#SBATCH --job-name=collect_seed_based_correlation   # Job name
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=8gb                   # Job Memory
#SBATCH --time=2:00:00             # Time limit hrs:min:sec
#SBATCH --output=./LOG_collect_seed_based_corr_hcp180.log    # Standard output and error log

module load bio/FSL/6.0.5.1-centos7_64

INPUTS=($(<../../data/subject_list.txt))
func () {
    f=$1
    echo $f >> seed_based_test.txt
    while read roi ; do
      all_values=""
      while read roi2 ; do
      	mean_value=`fslstats ../../data/resting/processed/seed_based_correlation/"$f"/"$roi"/dr_stage2_subject00000.nii.gz\
      	-k ../../data/resting/roi/"$f"/"$roi2".nii.gz -m`
	      all_values="$all_values $mean_value"
      done < ../../data/roi_names.txt
      echo $roi $all_values >> ../../data/resting/processed/seed_based_correlation/"$f".txt
    done < ../../data/roi_names.txt
}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"

