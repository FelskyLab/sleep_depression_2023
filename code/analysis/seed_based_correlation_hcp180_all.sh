START=0
STEP=2
SLEEP=1200 #20 min (in seconds)

INPUTS=($(<../../data/subject_list.txt))
END=$[ ${#INPUTS[@]} ]
echo $END

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ]
    echo "Submitting with ${JSTART} and ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} seed_based_correlation_hcp180.sh
    sleep $SLEEP
done


