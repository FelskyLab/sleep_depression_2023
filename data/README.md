# Data

Data can be acquired from [UK Biobank](https://www.ukbiobank.ac.uk/enable-your-research/apply-for-access) and [Human Connectome Project](https://www.humanconnectome.org/) websites through application processes. 
You have to add this data to the folders as described below to be able to run the full pipeline.
You can alternatively add the model coefficient files which can be downloaded from the supplementary data in the paper (link will be added upon publication) and plot the figures directly.

> **Note**
> Data is not included here and is substantially large sized.

## Task

Contains the task-based data. It is composed of five folders as follows:
```bash
task
├── activation            # <-- Contains the NIFTI files of the brain data loaded from UK Biobank 
├── behavior              # <-- Contains the stimulus information and behavioral results
│   ├── raw         # <-- txt files that are loaded from UK Biobank
│   └── csv         # <-- This will be populated with the converted data files to csv format
├── roi                   # <-- This is where the region masks will be stored when transformed            
├── processed             # <-- This is where the processed brain data will be generated
│   ├── decoding_accuracy      # <-- Results of the brain decoding analysis 
│   └── rsa                    # <-- Results for the representational connectivity analysis
└── stats                  # <-- This is where the association statistical tables will reside  
```   

## Resting

Contains the resting state data. It is composed of four folders as follows:
```bash
resting
├── activation            # <-- Contains the NIFTI files of the brain data loaded from UK Biobank 
├── roi                   # <-- This is where the region masks will be stored when transformed            
├── processed             # <-- This is where the processed brain data will be generated 
│   ├── functional_connectivity      # <-- Results of the functional connectivity analysis 
│   └── seed_based_correlation        # <-- Results for the seed-based connectivity analysis
└── stats                  # <-- This is where the association statistical tables will reside
```   

## Anatomy

Contains the subject anatomy data in Freesufer format in addition to fsaverage.

## Phenotype

Contains the oype and covariate data. You want to add three files as follows:
```bash
resting
├── tfmri_data_covariates_221205.csv    # <-- All the five sleep, depression, and cognition variables 
├── covariates_task_230123.csv          # <-- The covariates that are used in the task models            
└── covariates_resting_230123.csv       # <-- The covariates that are used in the resting-state models
```   

## Helper files
There are a group of helper files that are utilized by the codes that you either have to include or are already included.
They live under the parent data folder as follows:
```bash
data
├── final_hcp180_roi_list_bilateral.txt    # <-- Contains ROI names in the original form 
├── roi_names.txt                          # <-- Contains ROI names in formatted without any - signs (messes up with bdpy and statsmodels)            
├── fMRI_volume_allocation.csv             # <-- Contains the fMRI volumes allocated to each stimulus in the task (essential for decoding analysis)
├── lh_vertex_means_pre.csv                # <-- Contains the midpoint of each ROI in fsaverage_pre space. Used to plot connectivity.
└── subject_list.txt                       # <-- Contains the subject IDs (each line is one ID), you have to add this yourself
``` 