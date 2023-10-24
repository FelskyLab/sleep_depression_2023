#!/bin/bash
#SBATCH --job-name=seed_based_correlation   # Job name
#SBATCH --mail-type=FAIL            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=mohamed.abdelhack@camh.ca   # Where to send mail	
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=8gb                   # Job Memory
#SBATCH --time=02:30:00             # Time limit hrs:min:sec
#SBATCH --output=./script_outputs/seed_based_corr_hcp180.log    # Standard output and error log

module load bio/FSL/6.0.5.1-centos7_64

INPUTS=($(<remaining_seed_subjects.txt))
#echo ${INPUTS[1]}
#my function
func () {
    f=$1
    echo $f
#    mkdir /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data/"$f"_20227_2_0/seed_based_correlation/
    while read roi ; do
      echo $roi
      dual_regression /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data_roi/hcp180/"$f"/"$roi".nii.gz 0 -1 0 \
      /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data/"$f"_20227_2_0/seed_based_correlation/"${roi//-/_}"\
      /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data/"$f"_20227_2_0/fMRI/rfMRI.ica/filtered_func_data_clean.nii.gz 
    done < /external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/hcp180/roi_names_rest.txt
}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"

