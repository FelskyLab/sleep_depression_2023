module load Freesurfer/6.0.0
SUBJECTS_DIR=/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/t1_surface/data/
for f in /external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/t1_surface/data/*_*_*
do
  filename="$(cut -d'/' -f11 <<< $f)"
  if [ -f "$f/label/lh.HCP-MMP.annot" ] && [ -f "$f/label/rh.HCP-MMP.annot" ] ; then
    labelfilecount=$(ls $f/label/hcp180/ | wc -l)
    echo $filename >> files_with_hcp180_labels.txt

    if test $((labelfilecount)) -lt 271; then
      echo $labelfilecount
      echo -e "\n\n------------Processing $filename file----------------\n\n"
      mkdir $f/label/hcp180/
      mri_annotation2label --subject $filename --hemi lh --annotation $f/label/lh.HCP-MMP.annot --outdir $f/label/hcp180/
      mri_annotation2label --subject $filename --hemi rh --annotation $f/label/rh.HCP-MMP.annot --outdir $f/label/hcp180/
    else
      echo "File $f already processed.. skipping"
    fi
 
  fi
  
done

