#!/bin/bash
#SBATCH --job-name=convert_label_to_resting_vol   # Job name
#SBATCH --mail-type=FAIL            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=mohamed.abdelhack@camh.ca   # Where to send mail	
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=1gb                   # Job Memory
#SBATCH --time=00:20:00             # Time limit hrs:min:sec
#SBATCH --output=./script_outputs/label_to_resting_vol_last.log    # Standard output and error log

module load Freesurfer/6.0.0
SUBJECTS_DIR=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/t1_surface/data

INPUTS=($(<subjects_with_missing_rois_vol_220715.txt))
#echo ${INPUTS[1]}
#my function
func () {
    f=$1
    tfmri=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data/"$f"_20227_2_0/
    filename="$(cut -d'/' -f12 <<< $f)"
    subject_id="$(cut -d'_' -f1 <<< $filename)"
    echo $subject_id
    labels_list=$SUBJECTS_DIR/fsaverage/label/hcp180/lh*.label

    label_location=(/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/t1_surface/data/"$subject_id"_20263_2_0/label/hcp180/?h.?_*.label)
    output_location=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data_roi/hcp180/"$filename"
    mkdir $output_location
    for label in "${label_location[@]}"
        do
          label_file="$(cut -d"/" -f14 <<< $label)"
          label_file="$(cut -d'.' -f2 <<< $label_file)"
#          echo "LOL"
#          echo $label
#          echo "$output_location"/"$label_file".nii.gz
          mri_label2vol --label "$label" --temp "$tfmri"/fMRI/rfMRI.ica/example_func.nii.gz --fillthresh 0.3  --regheader "$SUBJECTS_DIR"/"$subject_id"_20263_2_0/mri/orig.mgz --o "$output_location"/"$label_file".nii.gz
        done


}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
