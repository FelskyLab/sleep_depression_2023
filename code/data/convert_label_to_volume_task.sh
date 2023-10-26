#!/bin/bash
#SBATCH --job-name=convert_label_to_vol_task   # Job name
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=1gb                   # Job Memory
#SBATCH --time=02:00:00             # Time limit hrs:min:sec
#SBATCH --output=./LOG_label_to_vol_task.log    # Standard output and error log

module load Freesurfer/6.0.0
SUBJECTS_DIR=../../data/anatomy

INPUTS=($(<../../data/subject_list.txt))
func () {
    subject_id=$1
    tfmri=../../data/task/activation/"$subject_id"_20249_2_0/
    echo $subject_id
    mkdir $SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/
    labels_list=$SUBJECTS_DIR/fsaverage/label/hcp180/lh*.label

    for label in $labels_list
    do
      label_file="$(cut -d"/" -f8 <<< $label)"
      echo $label_file
      mri_label2label --srcsubject fsaverage --srclabel $label --trgsubject "$subject_id"_20263_2_0 --trglabel $SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/$label_file --regmethod surface --hemi lh
    done

    labels_list=$SUBJECTS_DIR/fsaverage/label/hcp180/rh*.label

    for label in $labels_list
    do
      label_file="$(cut -d"/" -f8 <<< $label)"
      mri_label2label --srcsubject fsaverage --srclabel $label --trgsubject "$subject_id"_20263_2_0 --trglabel $SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/$label_file --regmethod surface --hemi rh
    done

    label_location=($SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/?h.?_*.label)
    existing_labels=${#label_location[@]}

    if [ ${existing_labels} -gt 360 ] && [ -f "$tfmri"/fMRI/tfMRI.feat/example_func.nii.gz ];  then

      output_location=../../data/task/roi/"$subject_id"
      if [ -d $output_location ]; then
        existing_files=$output_location/*.nii.gz
      fi
      if [ ! -d $output_location ] || [ ${#existing_files[@]} -lt 360 ]; then
        mkdir $output_location
        for label in "${label_location[@]}"
        do
          label_file="$(cut -d"/" -f8 <<< $label)"
          label_file="$(cut -d'.' -f2 <<< $label_file)"
          mri_label2vol --label "$label" --temp "$tfmri"/fMRI/tfMRI.feat/example_func.nii.gz --fillthresh 0.3  --regheader "$SUBJECTS_DIR"/"$subject_id"_20263_2_0/mri/orig.mgz --o "$output_location"/"$label_file".nii.gz
        done

      fi
    fi

}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
