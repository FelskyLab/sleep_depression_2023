import pandas as pd
from glob import glob
import numpy as np
from tqdm import tqdm

with open('../../data/subject_list.txt', 'r') as f:
    subject_list = f.readlines()
subject_list = [s.strip() for s in subject_list]
print('Found', len(subject_list), 'subjects')

aggregated_data = pd.DataFrame(index=subject_list, columns=np.arange(210))
for idx, subject in tqdm(enumerate(subject_list)):
    filename = '../../data/resting/processed/functional_connectivity/{}_25750_2_0.txt'.format(subject)
    data_df = pd.read_csv(filename, delimiter=' ', header=None)
    aggregated_data.loc[subject, :] = data_df.dropna(axis=1).values

aggregated_data.to_csv('../../data/resting/processed/functional_connectivity_results.csv')