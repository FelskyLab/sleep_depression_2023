import os

from bdpy_make_dataset import get_data_locations, make_dataset
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.svm import SVC
import numpy as np
import pandas as pd
import pickle

def run_svm_model(subject_id, roi_list, options, model_options, save_model=False):
    data_loc, roi_loc, task_loc = get_data_locations(subject_id, roi_list)
    brain_data = make_dataset(data_loc, roi_loc, task_loc, options)
    # if ('motion_data' in model_options.keys()) and (model_options['motion_data']):
    #     motion_data = get_motion_data(subject_id)

    number_of_splits = model_options['number_of_splits']
    classification_target = model_options['classification_target']
    roi_list = model_options['roi_list']
    if roi_list == 'all':
        roi_list = get_all_rois(brain_data.metadata.key)
    split_object = StratifiedShuffleSplit(n_splits=number_of_splits,
                                          train_size=(number_of_splits - 1)/number_of_splits,
                                          test_size=1/number_of_splits,
                                          random_state=0)

    y = brain_data.get(classification_target)
    if 'target_dictionary' in model_options.keys():
        target_dictionary = model_options['target_dictionary']
        y = np.expand_dims(pd.Series(y.squeeze()).replace(target_dictionary).values, axis=1)
    filter_in_values = ~np.isnan(y.astype(float))
    y = y[filter_in_values]
    blocks = np.arange(y.shape[0])
    accuracy_list = pd.DataFrame(columns=roi_list, index=np.arange(number_of_splits), dtype=float)
    for idx, (train_index, test_index) in enumerate(split_object.split(blocks, y)):
        for roi in roi_list:
            voxels = brain_data.select(roi)
            voxels = voxels[filter_in_values.squeeze(), :]

            train_voxels = voxels[train_index, :]
            test_voxels = voxels[test_index, :]

            train_label = y[train_index]
            test_label = y[test_index]

            model = SVC(C=1.0,
                        kernel='linear',
                        verbose=False,
                        probability=True)
            model.fit(train_voxels, train_label.ravel())
            y_pred = model.predict(test_voxels)
            y_pred_proba = model.predict_proba(test_voxels)
            accuracy = model.score(test_voxels, test_label.ravel())
            accuracy_list.loc[idx, roi] = accuracy
            if save_model:
                save_folder = '/external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/svm_models/{}/{}/'.format(subject_id, roi)
                os.makedirs(save_folder, exist_ok=True)
                filename = os.path.join(save_folder, 'svm_model_cvsplit{}_{}.sav'.format(idx, classification_target))
                pickle.dump(model, open(filename, 'wb'))

    accuracy_list.index.name = 'cv_fold'
    return accuracy_list

def get_roi_list(roi_folders, combine_LR=False, suffices=None):
    roi_list_formatted = list()
    if suffices is None:
        suffices = ['' for x in range(len(roi_folders))]
    for roi_folder, suffix in zip(roi_folders, suffices):
        roi_list_file = 'final_{}_roi_list{}.txt'.format(roi_folder, suffix)
        with open(roi_list_file) as f:
            roi_list = f.readlines()
        file_roi_list = [s.strip() for s in roi_list]
        for roi in file_roi_list:
            if combine_LR:
                if all(['L' + roi[1:] in file_roi_list,  'R' + roi[1:] in file_roi_list]):
                    roi_name = 'roi_{}_L{} + roi_{}_R{}'.format(roi_folder, roi[1:], roi_folder, roi[1:])
                else:
                    roi_name = 'roi_{}_{}'.format(roi_folder, roi)
            else:
                roi_name = 'roi_{}_{}'.format(roi_folder, roi)
            roi_list_formatted.append(roi_name)
            roi_list_formatted = list(set(roi_list_formatted))
    return roi_list_formatted

def get_all_rois(metadata_keys, combine_LR=False):
    roi_list_formatted = [metadata_key for metadata_key in metadata_keys if metadata_key.startswith('roi_')]
    if combine_LR:
        roi_name = [roi.split('_', 2)[2] for roi in roi_list_formatted]
        roi_folders = [roi.split('_', 2)[1] for roi in roi_list_formatted]
        roi_list_formatted = ['roi_{}_L{} + roi_{}_R{}'.format(roi_folder, roi[1:], roi_folder, roi[1:]) \
                                  if all(['L' + roi[1:] in roi_name,  'R' + roi[1:] in roi_name])\
                                  else 'roi_{}_{}'.format(roi_folder, roi)\
                              for roi, roi_folder in zip(roi_name, roi_folders)]
    roi_list_formatted = list(set(roi_list_formatted))
    return roi_list_formatted

if __name__ == '__main__':
    import time
    import resource

    start_time = time.time()
    subject = '4693901' # 1432072 #{'3237551', '3701308', '4099348', '4568736', '5633652'}
    rois_in_bdata = ['aseg', 'hcp180']
    opts = dict()
    opts['shift_size'] = 5
    opts['normalize_mode'] = 'PercentSignalChange'
    opts['voxel_coordinate_rounding'] = 3
    model_construction = dict()
    model_construction['number_of_splits'] = 6
    model_construction['classification_target'] = 'emotion_binary'
    # model_construction['target_dictionary'] = {'Non-face':np.nan, 'fear':0, 'anger':1}
    # model_construction['roi_list'] = 'all'
    model_construction['roi_list'] = get_roi_list(['hcp180'], combine_LR=False, suffices=['_bilateral'])
    model_construction['roi_list'].extend(get_roi_list(['aseg'], combine_LR=True))
    # model_construction['motion_data'] = True
    accuracy_df = run_svm_model(subject, rois_in_bdata, opts, model_construction, save_model=True)
    print(accuracy_df.describe(percentiles=[]))
    print("--- %s seconds elapsed ---" % (time.time() - start_time))
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)


