START=0
STEP=2
SLEEP=1200 #20 Minutes (in seconds)

INPUTS=($(<../../data/subject_list.txt))
END=$[ ${#INPUTS[@]} ]
echo $END

for i in $(seq $START $STEP $END) ; do
    JSTART=$i
    JEND=$[ $STEP - 1 ] 
    echo "Submitting with ${JSTART} and ${JEND}"
    sbatch --array=0-${JEND} --export=f1=${JSTART} make_rdsa_shp_sex_emotion.sh
    sleep $SLEEP
done
