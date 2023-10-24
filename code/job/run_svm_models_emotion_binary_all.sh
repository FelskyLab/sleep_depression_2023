START=0
STEP=70
SLEEP=1800 #20 Minutes (in seconds)

INPUTS=($(<subjects_remaining_hcp_emotion_binary_svm_subjects_220716.txt))
END=$[ ${#INPUTS[@]} ]
echo $END

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ] 
    echo "Submitting with ${JSTART} and ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} run_svm_models_emotion_binary.sh
    sleep $SLEEP
done
