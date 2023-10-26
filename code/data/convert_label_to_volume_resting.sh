#!/bin/bash
#SBATCH --job-name=convert_label_to_vol_resting # Job name
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=1gb                   # Job Memory
#SBATCH --time=00:20:00             # Time limit hrs:min:sec
#SBATCH --output=./LOG_label_to_vol_resting.log    # Standard output and error log

module load Freesurfer/6.0.0
SUBJECTS_DIR=../../data/anatomy

INPUTS=($(<../../data/subject_list.txt))

func () {
    subject_id=$1
    tfmri=../../data/resting/activation/"$subject_id"_20227_2_0/
    echo $subject_id

    label_location=($SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/?h.?_*.label)
    output_location=../../data/resting/roi/"$subject_id"
    mkdir $output_location
    for label in "${label_location[@]}"
        do
          label_file="$(cut -d"/" -f8 <<< $label)"
          label_file="$(cut -d'.' -f2 <<< $label_file)"
          mri_label2vol --label "$label" --temp "$tfmri"/fMRI/rfMRI.ica/example_func.nii.gz --fillthresh 0.3  --regheader "$SUBJECTS_DIR"/"$subject_id"_20263_2_0/mri/orig.mgz --o "$output_location"/"$label_file".nii.gz
        done

}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
