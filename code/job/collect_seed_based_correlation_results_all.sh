START=0
STEP=31
SLEEP=1800 #0.5 hours (in seconds)

INPUTS=($(<remaining_collect_seed_based_subjects2.txt))
END=$[ ${#INPUTS[@]} ]
echo $END

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ]
    echo "Submitting with ${JSTART} and ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} collect_seed_based_correlation_results.sh
    sleep $SLEEP
done


