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
    f=$1
    tfmri=../../data/resting/activation/"$f"_20227_2_0/
    filename="$(cut -d'/' -f12 <<< $f)"
    subject_id="$(cut -d'_' -f1 <<< $filename)"
    echo $subject_id
    labels_list=$SUBJECTS_DIR/fsaverage/label/hcp180/lh*.label

    label_location=($SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/?h.?_*.label)
    output_location=../../data/resting/roi/"$filename"
    mkdir $output_location
    for label in "${label_location[@]}"
        do
          label_file="$(cut -d"/" -f14 <<< $label)"
          label_file="$(cut -d'.' -f2 <<< $label_file)"
          mri_label2vol --label "$label" --temp "$tfmri"/fMRI/rfMRI.ica/example_func.nii.gz --fillthresh 0.3  --regheader "$SUBJECTS_DIR"/"$subject_id"_20263_2_0/mri/orig.mgz --o "$output_location"/"$label_file".nii.gz
        done

}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
