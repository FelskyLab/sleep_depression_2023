START=0
STEP=90
SLEEP=3600 #60 Minutes (in seconds)

INPUTS=($(<remaining_subjects_hcp180_annotation_220708.txt))
END=$[ ${#INPUTS[@]} ]
echo ${#INPUTS[@]}

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ] 
    echo "Submitting from ${JSTART} and step= ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} convert_all_labels_to_volume.sh
    sleep $SLEEP
done
