import pandas as pd
from os import path
from glob import glob

data_location = '../../data/task/behavior'
output_files_folder = 'csv'

response_summary = pd.DataFrame(columns=['accuracy_mean', 'accuracy_std', 'response_time_mean', 'response_time_std'])
experiment_timing_list = glob(path.join(data_location, output_files_folder,'*.csv'))
for timing_file in experiment_timing_list:
    subject_id = timing_file.split('/')[-1]
    subject_id = subject_id.split('_')[0]
    experiment_timing = pd.read_csv(timing_file)
    response_summary.loc[subject_id, 'accuracy_mean'] = experiment_timing['accuracy'].mean()
    response_summary.loc[subject_id, 'accuracy_std'] = experiment_timing['accuracy'].std()
    response_summary.loc[subject_id, 'response_time_mean'] = experiment_timing['response_time'].mean()
    response_summary.loc[subject_id, 'response_time_std'] = experiment_timing['response_time'].std()
response_summary.to_csv(path.join(data_location,'task_fmri_response_summary.csv'))
