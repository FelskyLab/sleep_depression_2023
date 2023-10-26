START=0
STEP=2
SLEEP=3600 #60 Minutes (in seconds)

INPUTS=($(<../../data/subject_list.txt))
END=$[ ${#INPUTS[@]} ]
echo ${#INPUTS[@]}

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ] 
    echo "Submitting from ${JSTART} and step= ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} convert_label_to_volume_task.sh
    sleep $SLEEP
done
