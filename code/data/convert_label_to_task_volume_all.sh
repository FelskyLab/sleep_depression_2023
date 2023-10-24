START=0
STEP=90
SLEEP=600 #10 Minutes (in seconds)

INPUTS=($(<subjects_with_missing_rois_vol_220713.txt))
END=$[ ${#INPUTS[@]} ]
echo ${#INPUTS[@]}

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ] 
    echo "Submitting from ${JSTART} and step= ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} convert_label_to_task_volume.sh
    sleep $SLEEP
done
