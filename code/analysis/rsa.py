import os
from bdpy_make_dataset import get_data_locations, make_dataset
import numpy as np
import pandas as pd
from svm_decoder_model import get_all_rois, get_roi_list

def calculate_rdsa(subject_id, options, model_options, save_model=False):
    data_loc, roi_loc, task_loc = get_data_locations(subject_id)
    brain_data = make_dataset(data_loc, roi_loc, task_loc, options)

    roi_list = model_options['roi_list']
    if roi_list == 'all':
        roi_list = get_all_rois(brain_data.metadata.key)

    classification_target = model_options['label']
    y = brain_data.get(classification_target)
    if 'target_dictionary' in model_options.keys():
        target_dictionary = model_options['target_dictionary']
        y = np.expand_dims(pd.Series(y.squeeze()).replace(target_dictionary).values, axis=1)
    filter_in_values = y != 'nan'
    y = y[filter_in_values]
    rdsa_roi = dict()
    for roi in roi_list:
        voxels = brain_data.select(roi)
        voxels = voxels[filter_in_values.squeeze(), :]
        voxels = create_averaged_voxel_stream(voxels, y, model_options['averaging_groups'])
        rdsa = 1 - np.corrcoef(voxels)
        rdsa_roi[roi] = rdsa
        if save_model:
            save_folder = '../../data/task/processed/rsa/{}/'.format(subject_id)
            os.makedirs(save_folder, exist_ok=True)
            filename = os.path.join(save_folder, 'rsa_{}.npy'.format(roi.replace(' ', '_')))
            np.save(filename, rdsa)
    return rdsa_roi

def create_averaged_voxel_stream(data, label, averaging_groups):
    averaged_voxel_data = np.zeros((len(averaging_groups), data.shape[1]))
    for idx, group in enumerate(averaging_groups):
        group_flag = pd.Series(data=label.squeeze()).str.contains('_' + group)
        averaged_voxel_data[idx, :] = np.mean(data[group_flag, :].astype(float), axis=0)
    return averaged_voxel_data

def multidimensional_scaling(rdsa_list):
    pass

def representational_connectivity(rdsa_roi, model_options, subject_id, save=False):
    connectivity_matrix = pd.DataFrame(columns=rdsa_roi.keys(), index=rdsa_roi.keys())
    for roi1 in rdsa_roi.keys():
        for roi2 in rdsa_roi.keys():
            data1 = rdsa_roi[roi1]
            data2 = rdsa_roi[roi2]
            rdsa_values1 = data1[np.triu_indices(data1.shape[0], k=1)]
            rdsa_values2 = data2[np.triu_indices(data1.shape[0], k=1)]
            connectivity_matrix.loc[roi1, roi2] = np.corrcoef(rdsa_values1, rdsa_values2)[0, 1]
    if save:
        save_folder = '../../data/task/processed/rsa/'
        filename = os.path.join(save_folder, '{}.csv'.format(subject_id))
        connectivity_matrix.to_csv(filename)
    return connectivity_matrix


if __name__ == '__main__':
    import time
    import resource

    start_time = time.time()
    subject = '4693901'
    print(subject)
    opts = dict()
    opts['shift_size'] = 5
    opts['normalize_mode'] = 'PercentSignalChange'
    opts['voxel_coordinate_rounding'] = 3
    model_construction = dict()
    model_construction['number_of_splits'] = 6
    model_construction['label'] = 'image_top'

    model_construction['target_dictionary'] = {'oval-vertical.bmp':'shape_ovalv',
                                               'oval-horizontal.bmp':'shape_ovalh',
                                               'circle.bmp': 'shape_circle',
                                               'MA2_top.jpg': 'face_male_anger',
                                               'MA1_top.jpg': 'face_male_anger',
                                               'MA3_top.jpg': 'face_male_anger',
                                               'MF1_top.jpg': 'face_male_fear',
                                               'MF2_top.jpg': 'face_male_fear',
                                               'MF3_top.jpg': 'face_male_fear',
                                               'FF1_top.jpg': 'face_female_fear',
                                               'FF2_top.jpg': 'face_female_fear',
                                               'FF3_top.jpg': 'face_female_fear',
                                               'FA1_top.jpg': 'face_female_anger',
                                               'FA2_top.jpg': 'face_female_anger',
                                               'FA3_top.jpg': 'face_female_anger'}
    model_construction['averaging_groups'] = ['circle', 'ovalv', 'ovalh', 'male', 'female', 'anger', 'fear']
    model_construction['large_groupings'] = {'shape':['circle', 'ovalv', 'ovalh'],
                                             'sex': ['male', 'female'],
                                             'emotion': ['anger', 'fear']}
    model_construction['rsa_type'] = 'shp_sex_emotion'
    model_construction['roi_list'] = get_roi_list(['hcp180'], combine_LR=False, suffices=['_bilateral'])
    rdsa_dict = calculate_rdsa(subject, opts, model_construction, save_model=False)
    representational_connectivity(rdsa_dict, model_construction, subject, save=True)
    print("--- %s seconds elapsed ---" % (time.time() - start_time))
    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)



