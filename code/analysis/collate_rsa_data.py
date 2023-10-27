import pandas as pd
from glob import glob
import numpy as np
from tqdm import tqdm

with open('../../data/subject_list.txt', 'r') as f:
    subject_list = f.readlines()
subject_list = [s.strip() for s in subject_list]
print('Found', len(subject_list), 'subjects')

with open('../../data/final_hcp180_roi_list_bilateral.txt', 'r') as f:
    roi_list = f.readlines()
roi_list = ['roi_hcp180_{}'.format(s.strip()) for s in roi_list]

aggregated_data = np.zeros((len(subject_list), 180, 180))
for idx, subject in tqdm(enumerate(subject_list)):
    filename = '../../data/task/processed/rsa/{}.csv'.format(subject)
    data_df = pd.read_csv(filename, index_col=0)
    data_df.drop_duplicates(inplace=True)
    data_df = data_df.loc[roi_list, roi_list]
    aggregated_data[idx, :, :] = data_df.values

np.save('../../data/task/processed/rsa_results.npy', aggregated_data)
