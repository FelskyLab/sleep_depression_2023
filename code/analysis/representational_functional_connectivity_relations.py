import numpy as np
import pandas as pd
import seaborn as sns
from bdpy.util import get_refdata


aggregated_results_rdsa = np.load('/external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/rdsa_connectivity_221206.npy')
print(aggregated_results_rdsa.shape)

with open('rdsa_rois.txt', 'r') as f:
    roi_list_rdsa = f.readlines()

roi_list_rdsa = [x.strip()[11:] for x in roi_list_rdsa[:-3]]
print(roi_list_rdsa)

with open('/external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/rdsa_subjects_221206.txt', 'r') as f:
    subject_list_rdsa = f.readlines()
subject_list_rdsa = [int(s.strip()) for s in subject_list_rdsa]
print(len(subject_list_rdsa))
print(subject_list_rdsa[0])

aggregated_results_seed = np.load('/external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/seed_based_correlation_results.npy')
aggregated_results_seed = aggregated_results_seed / np.tile(np.reshape(np.diagonal(aggregated_results_seed, 0, 1, 2), (30949, 180, 1)), (1,1,180))
aggregated_results_seed[np.isinf(aggregated_results_seed)] = np.nan
# aggregated_results_seed = aggregated_results_seed/2 + np.transpose(aggregated_results_seed, (0, 2, 1))/2
zero_abs = np.abs(aggregated_results_seed - np.nanmean(aggregated_results_seed, axis=(1,2), keepdims=True))
std_vals = np.nanstd(aggregated_results_seed, axis=(1,2), keepdims=True)
max_devs = 2.0
aggregated_results_seed[zero_abs > max_devs*std_vals] = np.nan
print(aggregated_results_seed.shape)

with open('/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/hcp180/roi_names_.txt', 'r') as f:
    roi_list_seed = f.readlines()
roi_list_seed = [s.strip() for s in roi_list_seed]
print(roi_list_seed)

with open('/external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/collected_subjects.txt', 'r') as f:
    subject_list_seed = f.readlines()
subject_list_seed = [int(s.strip()) for s in subject_list_seed]
print(len(subject_list_seed))
print(subject_list_seed[0])

aggregated_results_seed_rearranged = get_refdata(aggregated_results_seed, np.array(subject_list_seed), np.array(subject_list_rdsa))
print(aggregated_results_seed_rearranged.shape)

roi_indices_conversions = [np.where(np.array(roi_list_seed) == i)[0][0] for i in np.array(roi_list_rdsa)]
aggregated_results_seed_rearranged_roi = aggregated_results_seed_rearranged[:, roi_indices_conversions, :]
aggregated_results_seed_rearranged_roi = aggregated_results_seed_rearranged_roi[:, :, roi_indices_conversions]
print(aggregated_results_seed_rearranged.shape)
print(aggregated_results_seed_rearranged_roi.shape)

for idx in range(aggregated_results_seed_rearranged_roi.shape[0]):
    np.fill_diagonal(aggregated_results_seed_rearranged_roi[idx, :, :], 1)
    
aggregated_results_seed_rearranged_flat = np.reshape(aggregated_results_seed_rearranged,
                                                     (aggregated_results_seed_rearranged.shape[0], -1))


aggregated_results_rdsa_flat = np.reshape(aggregated_results_rdsa,
                                          (aggregated_results_rdsa.shape[0], -1))

correlation_values = list()
for idx in range(aggregated_results_rdsa_flat.shape[0]):
    corr_val = pd.DataFrame(aggregated_results_seed_rearranged_flat[idx,:]).corrwith(pd.DataFrame(aggregated_results_rdsa_flat[idx,:]))
    correlation_values.append(corr_val)
    
correlation_values_df = pd.DataFrame(data=correlation_values, index=subject_list_rdsa)
correlation_values_df.index.rename('eid', inplace=True)
correlation_values_df.columns= ['corr']
correlation_values_df

correlation_values_df.to_csv('representational_functional_connectivity_correlation.csv')

mean_difference = np.nanmean(np.abs(aggregated_results_seed_rearranged_flat - aggregated_results_rdsa_flat), axis=1)

mean_difference_df = pd.DataFrame(data=mean_difference, index=subject_list_rdsa)
mean_difference_df.index.rename('eid', inplace=True)
mean_difference_df.columns= ['mean_difference']
mean_difference_df
mean_difference_df.to_csv('representational_functional_connectivity_mean_difference.csv')

mean_resting = np.nanmean(aggregated_results_seed_rearranged_flat, axis=1)
mean_resting_df = pd.DataFrame(data=mean_resting, index=subject_list_rdsa)
mean_resting_df.index.rename('eid', inplace=True)
mean_resting_df.columns= ['mean_resting']
mean_resting_df

mean_resting_df.to_csv('representational_functional_connectivity_mean_resting.csv')

mean_task = np.nanmean(aggregated_results_rdsa_flat, axis=1)
mean_task_df = pd.DataFrame(data=mean_task, index=subject_list_rdsa)
mean_task_df.index.rename('eid', inplace=True)
mean_task_df.columns= ['mean_task']
mean_task_df

mean_task_df.to_csv('representational_functional_connectivity_mean_task.csv')

std_resting = np.nanstd(aggregated_results_seed_rearranged_flat, axis=1)
std_resting_df = pd.DataFrame(data=std_resting, index=subject_list_rdsa)
std_resting_df.index.rename('eid', inplace=True)
std_resting_df.columns= ['std_resting']
std_resting_df

std_resting_df.to_csv('representational_functional_connectivity_std_resting.csv')

std_task = np.nanstd(aggregated_results_rdsa_flat, axis=1)
std_task_df = pd.DataFrame(data=std_task, index=subject_list_rdsa)
std_task_df.index.rename('eid', inplace=True)
std_task_df.columns= ['std_task']
std_task_df

std_task_df.to_csv('representational_functional_connectivity_std_task.csv')

summary_stats = pd.concat([correlation_values_df, mean_difference_df, mean_resting_df, std_resting_df, mean_task_df, std_task_df], axis=1)
summary_stats.to_csv('representational_functional_connectivity_summary_stats_230109.csv')

summary_stats.info()