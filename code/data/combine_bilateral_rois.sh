#!/bin/bash
#SBATCH --job-name=combine_bilateral_rois   # Job name
#SBATCH --mail-type=FAIL            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=mohamed.abdelhack@camh.ca   # Where to send mail	
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=1gb                   # Job Memory
#SBATCH --time=00:20:00             # Time limit hrs:min:sec
#SBATCH --output=./script_outputs/combine_bilateral_rois_resting.log    # Standard output and error log

module load bio/FSL/6.0.5.1-centos7_64
export SUBJECTS_DIR=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data_roi/hcp180
ROIS='/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/hcp180/roi_names.txt'
SUBJECTS='/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/valid_subjects_fmri_220722.txt'

INPUTS=($(<remaining_bilateral_resting.txt))
#echo ${INPUTS[1]}
#my function
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
