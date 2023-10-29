import pandas as pd
import numpy as np
import statsmodels.formula.api as smf

def model_connectivity_OLS(data_df, covariate_df, independent_var_df, independent_var):
    p_values = np.zeros((210, 1))
    t_values = np.zeros((210, 1))
    b_values = np.zeros((210, 1))
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
    return p_values, t_values, b_values

aggregated_results = pd.read_csv('../../data/resting/processed/functional_connectivity_results.csv', index_col=0)

#Load phenotypes
covariates_resting_df = pd.read_csv('../../data/phenotype/covariates_resting_230123.csv', index_col='eid')
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
                                 index=np.arange(210 * 5))

for idx, indep_var in enumerate(['duration_of_longest_sleep_bout',
                                 'phq2',
                                 'Number_of_symbol_digit_matches_made_correctly',
                                 'Sleeplessness___insomnia',
                                 'Daytime_dozing___sleeping_narcolepsy']):
    pval, tval, bval = model_connectivity_OLS(aggregated_results, covariates_resting_df, indep_vars_df, indep_var)
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 'Variable'] = variables_presentable[idx]
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 'Node 1'] = np.triu_indices(21, 1)[0]
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 'Node 2'] = np.triu_indices(21, 1)[1]
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 'Coefficient'] = bval.squeeze()
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 't-value'] = tval.squeeze()
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 'p-value (raw)'] = pval.squeeze()
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 'p-value (Bonferroni)'] = pval.squeeze() * 5 * 21
    assoc_stats_df.loc[idx * 210:(idx + 1) * 210 - 1, 'Significant'] = pval.squeeze() * 5 * 21 < 0.05
assoc_stats_df.to_csv('../../data/resting/stats/functional_connectivity_association_statistics.csv', index=False)

