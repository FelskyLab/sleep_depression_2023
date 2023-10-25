#!/bin/bash
#SBATCH --job-name=combine_bilateral_rois   # Job name
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=1gb                   # Job Memory
#SBATCH --time=00:20:00             # Time limit hrs:min:sec
#SBATCH --output=./LOG_combine_bilateral_rois.log    # Standard output and error log

module load bio/FSL/6.0.5.1-centos7_64
export SUBJECTS_DIR=../../data/resting/roi/
ROIS='../../data/roi_names.txt'
SUBJECTS='../../data/subject_list.txt'

INPUTS=($(<../../data/subject_list.txt))

func () {
    f=$1
  echo $f
  while read roi;
  do
    fslmaths "$SUBJECTS_DIR"/"$f"/L_"$roi".nii.gz -add "$SUBJECTS_DIR"/"$f"/R_"$roi".nii.gz "$SUBJECTS_DIR"/"$f"/"$roi".nii.gz
  done < "$ROIS"

}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
