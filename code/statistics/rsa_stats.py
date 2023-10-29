import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

def model_connectivity_OLS(data_df, subject_list, covariate_df, independent_var_df, independent_var):
    p_values = np.zeros((180, 180))
    t_values = np.zeros((180, 180))
    b_values = np.zeros((180, 180))
    for idx1 in range(179):
        print(idx1)
        for idx2 in range(idx1 + 1, 180):
            data = pd.Series(data_df[:, idx1, idx2], index=subject_list)
            covariate_df['data'] = data
            covariate_df[independent_var] = independent_var_df[independent_var]
            model_string = 'data ~ {} + C(site) + age + C(sex) + age:C(sex) + ses + C(ethnicity) + education + head_motion'.format(
                    independent_var)
            if independent_var == 'duration_of_longest_sleep_bout': # if actigraphy data add difference in time
                model_string = model_string + ' + actigraphy_time'
            lr_model = smf.ols(model_string, data=covariate_df)

            lr_results = lr_model.fit()

            p_values[idx1, idx2] = lr_results.pvalues[independent_var]
            t_values[idx1, idx2] = lr_results.tvalues[independent_var]
            b_values[idx1, idx2] = lr_results.params[independent_var]
    return p_values, t_values, b_values

aggregated_results = np.load('../../data/task/processed/rsa_results.npy')

with open('../../data/subject_list.txt', 'r') as f:
    collected_subject_list = f.readlines()
collected_subject_list = [int(s.strip()) for s in collected_subject_list]

with open('../../data/final_hcp180_roi_list_bilateral.txt', 'r') as f:
    roi_list = f.readlines()
roi_list = [s.strip() for s in roi_list]
roi_list_presentable = [x[:-4].replace('_', '-') for x in roi_list]

# Normalization
aggregated_results_norm = aggregated_results / np.tile(np.reshape(np.diagonal(aggregated_results, 0, 1, 2), (len(collected_subject_list), 180, 1)), (1,1,180))

# Removal of invalid data
aggregated_results_norm[np.isinf(aggregated_results_norm)] = np.nan

# Forcing symmetry
aggregated_results_norm = aggregated_results_norm/2 + np.transpose(aggregated_results_norm, (0, 2, 1))/2

# Remove outliers
zero_abs = np.abs(aggregated_results_norm - np.nanmean(aggregated_results_norm, axis=(1,2), keepdims=True))
std_vals = np.nanstd(aggregated_results_norm, axis=(1,2), keepdims=True)
max_devs = 2.0
aggregated_results_norm[zero_abs > max_devs*std_vals] = np.nan

#Load phenotypes
covariates_resting_df = pd.read_csv('../../data/phenotype/covariates_task_230123.csv', index_col='eid')
covariates_resting_df['sex'] = covariates_resting_df['sex'].astype("category")
covariates_resting_df['site'] = covariates_resting_df['site'].astype("category")
covariates_resting_df['ethnicity'] = covariates_resting_df['ethnicity'].astype("category")
covariates_resting_df['age'] = (covariates_resting_df['age'] - covariates_resting_df['age'].mean()) / covariates_resting_df['age'].std()
covariates_resting_df['ses'] = (covariates_resting_df['ses'] - covariates_resting_df['ses'].mean()) / covariates_resting_df['ses'].std()
covariates_resting_df['education'] = (covariates_resting_df['education'] - covariates_resting_df['education'].mean()) / covariates_resting_df['education'].std()
covariates_resting_df['actigraphy_time'] = (covariates_resting_df['actigraphy_time'] - covariates_resting_df['actigraphy_time'].mean()) / covariates_resting_df['actigraphy_time'].std()
covariates_resting_df['head_motion'] = (covariates_resting_df['head_motion'] - covariates_resting_df['head_motion'].mean()) / covariates_resting_df['head_motion'].std()

indep_vars_df = pd.read_csv('../../data/phenotype/tfmri_data_covariates_221205.csv', index_col='eid', usecols=['eid', 'duration_of_longest_sleep_bout', 'phq2', 'Number_of_symbol_digit_matches_made_correctly', 'Sleeplessness___insomnia', 'Daytime_dozing___sleeping_narcolepsy'])

variables_presentable = ['Duration of longest sleep bout', 'PHQ-2', 'Cognition', 'Self-report insomnia', 'Self-report daytime dozing']
assoc_stats_df = pd.DataFrame(columns=['Variable', 'Node 1', 'Node 2', 'Coefficient', 't-value', 'p-value (raw)', 'p-value (Bonferroni)', 'Significant'],
                                 index=np.arange(16110 * 5))

for idx, indep_var in enumerate(['duration_of_longest_sleep_bout',
                                 'phq2',
                                 'Number_of_symbol_digit_matches_made_correctly',
                                 'Sleeplessness___insomnia',
                                 'Daytime_dozing___sleeping_narcolepsy']):
    pval, tval, bval = model_connectivity_OLS(aggregated_results_norm, collected_subject_list, covariates_resting_df, indep_vars_df, indep_var)
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 'Variable'] = variables_presentable[idx]
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 'Node 1'] = np.array(roi_list_presentable)[
        np.triu_indices(180, 1)[0]]
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 'Node 2'] = np.array(roi_list_presentable)[
        np.triu_indices(180, 1)[1]]
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 'Coefficient'] = bval[np.triu_indices(180, 1)]
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 't-value'] = tval[np.triu_indices(180, 1)]
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 'p-value (raw)'] = pval[np.triu_indices(180, 1)]
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 'p-value (Bonferroni)'] = pval[
                                                                                        np.triu_indices(180, 1)] * 5
    assoc_stats_df.loc[idx * 16110:(idx + 1) * 16110 - 1, 'Significant'] = pval[np.triu_indices(180, 1)] * 5 < 0.05
assoc_stats_df.to_csv('../../data/task/stats/rsa_association_statistics.csv', index=False)

