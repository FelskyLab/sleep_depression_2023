#!/bin/bash
#SBATCH --job-name=convert_label_to_vol_all   # Job name
#SBATCH --mail-type=FAIL            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=mohamed.abdelhack@camh.ca   # Where to send mail	
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=1gb                   # Job Memory
#SBATCH --time=02:00:00             # Time limit hrs:min:sec
#SBATCH --output=./script_outputs/label_to_vol_last.log    # Standard output and error log

module load Freesurfer/6.0.0
SUBJECTS_DIR=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/t1_surface/data

INPUTS=($(<remaining_subjects_hcp180_annotation_220708.txt))
#echo ${INPUTS[1]}
#my function
func () {
    f=$1
    tfmri=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_task_based/nifti/data/"$f"_20249_2_0/
    filename="$(cut -d'/' -f12 <<< $f)"
    subject_id="$(cut -d'_' -f1 <<< $filename)"
    echo $subject_id
    labels_list=$SUBJECTS_DIR/fsaverage/label/hcp180/lh*.label

	for label in $labels_list
	do
		label_file="$(cut -d"/" -f14 <<< $label)"
#		echo $label
#		echo $label_file
		mri_label2label --srcsubject fsaverage --srclabel $label --trgsubject "$subject_id"_20263_2_0 --trglabel $SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/$label_file --regmethod surface --hemi lh 
	done

	labels_list=$SUBJECTS_DIR/fsaverage/label/hcp180/rh*.label

	for label in $labels_list
	do
 		label_file="$(cut -d"/" -f14 <<< $label)"
#        	echo $label
#       		 echo $label_file
        	mri_label2label --srcsubject fsaverage --srclabel $label --trgsubject "$subject_id"_20263_2_0 --trglabel $SUBJECTS_DIR/"$subject_id"_20263_2_0/label/hcp180/$label_file --regmethod surface --hemi rh
	done

    label_location=(/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/t1_surface/data/"$subject_id"_20263_2_0/label/hcp180/?h.?_*.label)
    existing_labels=${#label_location[@]}
#    echo $existing_labels
#    echo $f
    if [ ${existing_labels} -gt 260 ] && [ -f "$tfmri"/fMRI/tfMRI.feat/example_func.nii.gz ];  then
      
      echo $subject_id >> files_with_hcp180_labels_tfmri_220618.txt

      output_location=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_task_based/nifti/data_roi/hcp180/"$filename"
      if [ -d $output_location ]; then
        existing_files=$output_location/*.nii.gz
      fi
      if [ ! -d $output_location ] || [ ${#existing_files[@]} -lt 271 ]; then
#        echo "We are here"
        mkdir $output_location
        for label in "${label_location[@]}"
        do
          label_file="$(cut -d"/" -f14 <<< $label)"
          label_file="$(cut -d'.' -f2 <<< $label_file)"
#          echo "LOL"
#          echo $label
#          echo "$output_location"/"$label_file".nii.gz
          mri_label2vol --label "$label" --temp "$tfmri"/fMRI/tfMRI.feat/example_func.nii.gz --fillthresh 0.3  --regheader "$SUBJECTS_DIR"/"$subject_id"_20263_2_0/mri/orig.mgz --o "$output_location"/"$label_file".nii.gz
        done

      fi
    fi

}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"
