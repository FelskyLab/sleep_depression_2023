import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import fdrcorrection

def model_connectivity_OLS(data_df, covariate_df, independent_var_df, independent_var):
    p_values = np.zeros((180, 1))
    p_values_fdr = np.zeros((180, 1))
    t_values = np.zeros((180, 1))
    b_values = np.zeros((180, 1))
    for idx1, roi in enumerate(data_df.columns):
        print(idx1)

        data = data_df[roi]
        covariate_df['data'] = data
        covariate_df[independent_var] = (independent_var_df[independent_var] - independent_var_df[independent_var].mean()) / independent_var_df[independent_var].std()
        model_string = 'data ~ {} + C(site) + age + C(sex) + age:C(sex) + ses + C(ethnicity) + education + head_motion'.format(
                independent_var)
        if independent_var == 'duration_of_longest_sleep_bout': # if actigraphy data add difference in time
            model_string = model_string + ' + actigraphy_time'
        lr_model = smf.ols(model_string, data=covariate_df)

        lr_results = lr_model.fit()

        p_values[idx1] = lr_results.pvalues[independent_var]
        t_values[idx1] = lr_results.tvalues[independent_var]
        b_values[idx1] = lr_results.params[independent_var]
        p_values_fdr[idx1] = fdrcorrection(lr_results.pvalues[independent_var], alpha=0.05, method='i')[1]
    return p_values, p_values_fdr, t_values, b_values

aggregated_results = pd.read_csv('../../data/task/processed/decoding_accuracy_results.csv', index_col=0)

with open('../../data/final_hcp180_roi_list_bilateral.txt', 'r') as f:
    roi_list = f.readlines()
roi_list = [s.strip() for s in roi_list]
roi_list_presentable = [x[:-4].replace('_', '-') for x in roi_list]

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
                                 index=np.arange(180 * 5))

for idx, indep_var in enumerate(['duration_of_longest_sleep_bout',
                                 'phq2',
                                 'Number_of_symbol_digit_matches_made_correctly',
                                 'Sleeplessness___insomnia',
                                 'Daytime_dozing___sleeping_narcolepsy']):
    pval, pval_fdr, tval, bval = model_connectivity_OLS(aggregated_results, covariates_resting_df, indep_vars_df, indep_var)
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 'Variable'] = variables_presentable[idx]
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 'ROI'] = np.array(roi_list_presentable)
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 'Coefficient'] = bval.squeeze()
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 't-value'] = tval.squeeze()
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 'p-value (raw)'] = pval.squeeze()
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 'p-value (FDR)'] = pval_fdr.squeeze()
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 'p-value (Bonferroni)'] = pval.squeeze() * 5
    assoc_stats_df.loc[idx * 180:(idx + 1) * 180 - 1, 'Significant'] = pval.squeeze() * 5 < 0.05
assoc_stats_df.to_csv('../../data/task/stats/decoding_association_statistics.csv', index=False)

