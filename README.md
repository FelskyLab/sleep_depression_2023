# Opposing brain signatures of sleep in task-based and resting-state conditions

This repo contains the code for reproducing the results of the paper [Opposing brain signatures of sleep in task-based and resting-state conditions](https://www.biorxiv.org/content/10.1101/2023.05.13.540646v3.abstract).
## Table of Contents

- [Table of Contents](#table-of-contents)
- [Abstract](#abstract)
- [How to use](#how-to-use)
- [Repository Structure](#repository-structure)

## Abstract

Sleep and depression have a complex, bidirectional relationship, with sleep-associated alterations in brain dynamics and structure impacting a range of symptoms and cognitive abilities. Previous work describing these relationships has provided an incomplete picture by investigating only one or two types of sleep measures, depression, or neuroimaging modalities in parallel. We analyzed the correlations between task and resting-state brain-wide signatures of sleep, cognition, and depression in over 30,000 individuals. Neural signatures of insomnia and depression were negatively correlated with neural signatures of sleep duration in the task condition but positively correlated in the resting-state condition, showing that resting-state neural signatures of insomnia and depression resemble that of rested wakefulness. This was further supported by our finding of hypoconnectivity in task but hyperconnectivity in resting-state data in association with insomnia and depression This information disputes conventional assumptions about the neurofunctional manifestations of hyper– and hypo-somnia, and may explain inconsistent findings in the literature.


## How to use
The project involves processing of [UK Biobank]() and [Human Connectome Project]() datasets. 
This code is catered to the UK Biobank analysis but it can be used with minimal modifications to process the HCP dataset.
You will need to add the data yourself into the respository (more on that [here](./data/README.md))
Please note that running the whole pipeline takes a really long time and it is better to run it in a cluster computer. 
The analysis are run in both bash and python 3.6.
It also uses tools from Freesurfer 6.0.0 and FSL 6.0.5.1 and they are loaded as modules as needed.
This code was run and tested on a cluster that uses Slurm Workload Manager for job scheduling and a Linux Centos 7 operating system.
After you add the data, you can run the codes based on the instructions [here](./code/README.md).

## Repository Structure

```bash
project-structure
├── .gitignore            # <-- Files and directories for git to ignore
├── code
│   ├── analysis    # <-- Code for performing analyses
│   ├── data        # <-- Code for roi conversion
│   └── figures     # <-- Code for producing figures
├── data            
│   ├── task      # <-- Data for the task condition
│   ├── resting      # <-- Data for the resting-state condition
│   └── anatomy        # <-- Subject data in Freesurfer format 
├── environments    # <-- Environments used with project (i.e. .env, environment.yml)
├── figures         # <-- Generated figures
└── README.md       
  
```