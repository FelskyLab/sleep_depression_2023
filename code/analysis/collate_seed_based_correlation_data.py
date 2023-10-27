import pandas as pd
from glob import glob
import numpy as np
from tqdm import tqdm

with open('../../data/subject_list.txt', 'r') as f:
    subject_list = f.readlines()
subject_list = [s.strip() for s in subject_list]
print('Found', len(subject_list), 'subjects')

with open('../../data/roi_names.txt', 'r') as f:
    roi_list = f.readlines()
roi_list = [s.strip() for s in roi_list]

aggregated_data = np.zeros((len(subject_list), 180, 180))
for idx, subject in tqdm(enumerate(subject_list)):
    filename = '../../data/resting/processed/seed_based_correlation/{}.txt'.format(subject)
    data_df = pd.read_csv(filename, delimiter=' ', header=None)
    data_df.drop_duplicates(inplace=True)
    data_df.set_index(0, inplace=True)
    data_df = data_df.loc[roi_list]
    aggregated_data[idx, :, :] = data_df.values

np.save('../../data/resting/processed/seed_based_correlation_results.npy', aggregated_data)
