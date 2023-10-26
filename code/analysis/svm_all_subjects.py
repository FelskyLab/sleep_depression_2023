from svm_decoder_model import get_roi_list, run_svm_model
import numpy as np
import os
import sys

classification_target = sys.argv[1]
subject = sys.argv[2]
opts = dict()
opts['shift_size'] = 5
opts['normalize_mode'] = 'PercentSignalChange'
opts['voxel_coordinate_rounding'] = 3
model_construction = dict()
if classification_target == 'emotion':
    model_construction['target_dictionary'] = {'Non-face': np.nan, 'fear': 0, 'anger': 1}
model_construction['number_of_splits'] = 6
model_construction['classification_target'] = classification_target
model_construction['roi_list'] = get_roi_list(['hcp180'], combine_LR=False, suffices=['_bilateral'])
print(subject)
accuracy_df = run_svm_model(subject, opts, model_construction, save_model=False)
save_location = '../../data/task/processed/decoding_accuracy'
os.makedirs(save_location, exist_ok=True)
accuracy_df.to_csv('{}/{}.csv'.format(save_location, subject))
