START=0
STEP=70
SLEEP=600 #2 Minutes (in seconds)

INPUTS=($(<../../data/subject_list.txt))
END=$[ ${#INPUTS[@]} ]
echo ${#INPUTS[@]}

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ] 
    echo "Submitting from ${JSTART} and step= ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} combine_bilateral_rois.sh
    sleep $SLEEP
done

