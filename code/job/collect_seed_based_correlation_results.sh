#!/bin/bash
#SBATCH --job-name=collect_seed_based_correlation   # Job name
#SBATCH --mail-type=FAIL            # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=mohamed.abdelhack@camh.ca   # Where to send mail	
#SBATCH --ntasks=1                  # Run a single task
#SBATCH --mem=8gb                   # Job Memory
#SBATCH --time=2:00:00             # Time limit hrs:min:sec
#SBATCH --output=./script_outputs/collect_seed_based_corr_hcp180_last.log    # Standard output and error log

module load bio/FSL/6.0.5.1-centos7_64

INPUTS=($(<remaining_collect_seed_based_subjects2.txt))
#echo ${INPUTS[1]}
#my function
func () {
    f=$1
    echo $f >> seed_based_test.txt
#    mkdir /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data/"$f"_20227_2_0/seed_based_correlation/
    while read roi ; do
      all_values=""
      while read roi2 ; do
#      	echo $roi >> seed_based_test.txt
#	echo $roi2 >> seed_based_test.txt
      	mean_value=`fslstats /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data/"$f"_20227_2_0/seed_based_correlation/"$roi"/dr_stage2_subject00000.nii.gz\
      	-k /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting/data_roi/hcp180/"$f"/"$roi2".nii.gz -m`
	all_values="$all_values $mean_value"
#	echo $roi $roi2 $mean_value >> /external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/seed_based_correlation/"$f".txt
#	echo $roi $roi2 $mean_value >> correlation_seed_test1.txt
      done < /external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/hcp180/roi_names.txt
      echo $roi $all_values >> /external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/seed_based_correlation/"$f".txt
    done < /external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/hcp180/roi_names_.txt
}

#launch job arrays
file=$[ $f1 + $SLURM_ARRAY_TASK_ID ]
func "${INPUTS[$file]}"

