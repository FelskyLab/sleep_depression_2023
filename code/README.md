# Code

This folder contains all the analysis codes.
To run them, you have to have python 3.6, Freesurfer 6.0.0, and FSL 6.0.5.1.
I use multiple python libraries that are all defined in the [requirements file](../requirements.txt).
The environment is called ```viz``` in the codes but you can change it in the bash files or before running the python files.
The codes run on the SLURM workload managed enabled [Specialized Computing Cluster](https://kcniconfluence.camh.ca/display/SCC) in the Centre for Addiction and Mental Health.
These codes take a very long time to run so I implemented a per-subject parallelization scheme.
Since you cannot submit ~30,000 jobs, I also created a job submission script that groups jobs into a predefined number (specified in the code) and runs the codes in batches of parallel subjects. 
You will find that each bash script has two versions with one always ending with ```all```.
That one is the job submission script.
I will only list the main codes and their purpose ignoring the job submission ones.

## Data
While the brain data is preprocessed already, to perform an ROI analysis as described in the paper, we need to transform the HCP180 ROIs to the space of the fMRI activations.
There are also some other data conversions that are done to ease the analysis.
The codes are mostly bash
To do that the following codes exist:
```bash
data
├── convert_label_to_volume_task.sh      # <-- Transforms HCP180 parcellation from fsaverage to each subject and converts it into masks for task data
├── convert_label_to_volume_resting.sh   # <-- Converts transformed parcellations (created in above script) it into masks for resting data
├── combine_bilateral_rois.sh            # <-- Combines each left and right hemisphere ROIs into one 
└── behavioral_xml_print.py              # <-- Converts behavioral data into csv format and aligns fMRI volumes
```

## Analysis
This codes is the one that performs the main analyses and collates the results for the subsequent statistical analyes.
You will find here the SVM decoder models, the seed-based correlation codes, and the representational similarity analysis codes.
To do that the following codes exist (not all files are listed here as some contain helper functions):
```bash
analysis
├── run_svm_models_emotion_binary.sh             # <-- Runs the SVM models and saves the performance data
├── seed_based_correlation_hcp180.sh             # <-- Runs the seed-based correlation
├── collect_seed_based_correlation_results.sh    # <-- Averages seed-based correlation results per ROI and creates the connectivity data 
├── make_rdsa_shp_sex_emotion.sh                 # <-- Runs the representational similarity analysis
├── collate_decoding_accuracy_data.py            # <-- Averages and collects the decoding performance data
├── collate_functional_connectivity_data.py      # <-- Collects the functional connectivity data
├── collate_seed_based_correlation_data.py       # <-- Collects the seed-based correlation data
└── collate_rsa_data.py                          # <-- Collects the representational similarity data
```

## Statistics
This folder contains four files that run the OLS models for each one of the four analyses.
It results in generating the association statistics in the stats folders for [task](../data/task/stats) and [resting-state](../data/resting/stats) data. 


## Figures
This contains two jupyter notebooks for figure generation.
```bash
analysis
├── make_correlation_figures.ipynb      # <-- Generates figure 4 in the paper (the UK Biobank part)
└── plot_connectivity.ipynb             # <-- Generates figure 6 in the paper (the connectivity plots)
```