from bdpy import BData
from bdpy.mri.load_mri import load_mri
from bdpy.mri import get_roiflag
from glob import glob
import os
from pandas import read_csv
from bdpy.util import create_groupvector
import bdpy.preproc.interface as preprocess
import numpy as np
import hashlib


def make_dataset(data_location, roi_locations, task_file, options, verbose=False):
    #options
    shift_size = options['shift_size']
    normalize_mode = options['normalize_mode']
    voxel_coordinate_rounding = options['voxel_coordinate_rounding']

    # Load data
    VoxelData, xyz, ijk = load_mri(data_location)

    #Task data
    task_data = read_csv(task_file)

    #Convert task columns to labels
    task_data = process_task_file(task_data, number_of_volumes=VoxelData.shape[0])
    labels, label_descriptions = choose_labels()
    label_data = select_labels_from_taskfile(task_data, labels)

    # add emotion binary variable
    task_data = add_column_replace(task_data, 'emotion_binary', 'emotion', {'Non-face': 0, 'anger': 1, 'fear': 1})

    #essential labels for preprocessing
    number_of_fmri_volumes = task_data['number_of_fmri_volumes'].astype(int).values
    blocks = create_groupvector(task_data['block_label'].values, number_of_fmri_volumes)
    rest = create_groupvector(task_data['rest_label'].values, number_of_fmri_volumes)
    runs = np.ones(VoxelData.shape[0])
    supporting_vectors = [blocks, rest, runs]

    ## preprocessing
    # shift
    if shift_size > 0:
        VoxelData, shift_ind = preprocess.shift_sample(VoxelData, group=runs, shift_size=shift_size, verbose=verbose)
        label_data = filter_inds(label_data, shift_ind, mode='keep')
        supporting_vectors = filter_inds(supporting_vectors, shift_ind, mode='keep')

    # deternd
    runs = supporting_vectors[2]
    VoxelData = preprocess.detrend_sample(VoxelData, group=runs, keep_mean=True, verbose=verbose)

    # normalize each voxel
    if normalize_mode is not None:
        VoxelData = preprocess.normalize_sample(VoxelData, group=runs, mode=normalize_mode, baseline='All',
                                     zero_threshold=1, verbose=verbose)

    # average samples within block
    blocks = supporting_vectors[0]
    VoxelData, average_inds = preprocess.average_sample(VoxelData, group=blocks, verbose=verbose)
    label_data = filter_inds(label_data, average_inds, mode='keep')
    supporting_vectors = filter_inds(supporting_vectors, average_inds, mode='keep')

    # remove non-stimulus labels
    rest = supporting_vectors[1]
    VoxelData = VoxelData[~rest, :]
    label_data = filter_inds(label_data, ~rest, mode='keep')

    # Add everything to BData instance
    bdata = BData()
    # add data
    if verbose:
        print('Adding Data...')
    bdata.add(VoxelData, 'VoxelData')
    bdata.set_metadatadescription('VoxelData', 'Task fmri data')

    # Add coordinates
    bdata.add_metadata('voxel_x', xyz[0, :], description='X coordinates of voxels')
    bdata.add_metadata('voxel_y', xyz[1, :], description='Y coordinates of voxels')
    bdata.add_metadata('voxel_z', xyz[2, :], description='Z coordinates of voxels')
    bdata.add_metadata('voxel_i', ijk[0, :], description='i coordinates of voxels')
    bdata.add_metadata('voxel_j', ijk[1, :], description='j coordinates of voxels')
    bdata.add_metadata('voxel_k', ijk[2, :], description='k coordinates of voxels')

    if verbose:
        print('Adding labels...')
    # Add label data
    for idx, label in enumerate(labels):
        bdata.add(label_data[idx], label)
        bdata.set_metadatadescription(label, label_descriptions[idx])

    # Load ROIs
    if verbose:
        print('Adding ROIs...')
    for roi_location in roi_locations:
        roi_files = glob(os.path.join(roi_location, '*.nii.gz'))
        roi_group = 'hcp180'
        for file in roi_files:
            bdata = add_roimask(bdata, file, roi_prefix='roi_{}'.format(roi_group), brain_data='VoxelData', verbose=verbose, round=voxel_coordinate_rounding)

    return bdata

def filter_inds(variable_list, inds, mode='keep'):
    for idx, variable in enumerate(variable_list):
        if mode == 'keep':
            variable = variable[inds]
        elif mode == 'remove':
            variable = np.delete(variable, inds)
        variable_list[idx] = variable
    return variable_list

def get_data_locations(subject):
    base_location = '../../data/task/'
    data_location = '{}/activation/{}_20249_2_0/fMRI/tfMRI.feat/filtered_func_data.nii.gz'.format(base_location, subject)
    task_file = '{}/behavior/csv/{}_25748_2_0.csv'.format(base_location, subject)
    roi_locations = list()
    roi_location = '{}/roi/{}/'.format(base_location, subject)
    roi_locations.append(roi_location)

    return data_location, roi_locations, task_file

def get_data_locations_resting(subject, roi_groups):
    base_location = '../../data/resting/'
    data_location = '{}/activation/{}_20227_2_0/fMRI/rfMRI.ica/filtered_func_data_clean.nii.gz'.format(base_location, subject)
    roi_locations = list()
    for roi in roi_groups:
        roi_location = '{}/roi/{}/{}/'.format(base_location, roi, subject)
        roi_locations.append(roi_location)

    return data_location, roi_locations


def process_task_file(task_dataframe, number_of_volumes=332):
    trailing_volume_count = number_of_volumes - task_dataframe['number_of_fmri_volumes'].sum()
    final_rest_row = {'label': 'FinalRest',
                      'emotion': 'Non-face',
                      'number_of_fmri_volumes': trailing_volume_count}
    task_dataframe = task_dataframe.append(final_rest_row, ignore_index=True)

    #this should have been done before
    task_dataframe['emotion_binary'] = task_dataframe['emotion']
    task_dataframe.replace({'emotion_binary': {'Non-face': 0, 'anger': 1, 'fear': 1}}, inplace=True)

    # for preprocessing labels
    task_dataframe['rest_label'] = task_dataframe['image_top'].isna()
    task_dataframe['block_label'] = np.arange(task_dataframe.shape[0])
    return task_dataframe

def select_labels_from_taskfile(task_dataframe, labels):
    label_list = list()
    number_of_fmri_volumes = task_dataframe['number_of_fmri_volumes'].astype(int).values
    for label in labels:
        label_data = create_groupvector(task_dataframe[label].values, number_of_fmri_volumes)
        label_list.append(label_data)
    return label_list

def choose_labels():
    label_list = ['emotion_binary', 'emotion', 'image_top', 'response', 'accuracy', 'response_time']
    label_descriptions = ['either face or no-face (Non-face=0, face=1)',
                          'emotion of face fear or anger (values: Non-face, fear, anger)',
                          'file name of the image that appear to the top',
                          'response of subject (left=1, right=2, Nan=No response)',
                          'accuracy of subject response (0=wrong or no response, 1=correct)',
                          'time taken by subject to respond in milliseconds (zero denotes no response)']
    return label_list, label_descriptions

def add_column_replace(task_dataframe, new_column, source, replace_dict):
    task_dataframe[new_column] = task_dataframe[source]
    task_dataframe.replace({new_column: replace_dict}, inplace=True)
    return task_dataframe

def add_roimask(bdata, roi_mask, roi_prefix='',
                brain_data='VoxelData', xyz=['voxel_x', 'voxel_y', 'voxel_z'],
                return_roi_flag=False,
                verbose=True,
                round=None):
    '''Add an ROI mask to `bdata`.

    Parameters
    ----------
    bdata : BData
    roi_mask : str or list
        ROI mask file(s).

    Returns
    -------
    bdata : BData
    '''

    if isinstance(roi_mask, str):
        roi_mask = [roi_mask]

    # Get voxel xyz coordinates in `bdata`
    voxel_xyz = np.vstack([bdata.get_metadata(xyz[0], where=brain_data),
                           bdata.get_metadata(xyz[1], where=brain_data),
                           bdata.get_metadata(xyz[2], where=brain_data)])
    if round is not None:
        voxel_xyz = np.round(voxel_xyz, round)

    # Load the ROI mask files
    mask_xyz_all = []
    mask_v_all = []

    voxel_consistency = True

    for m in roi_mask:
        mask_v, mask_xyz, mask_ijk = load_mri(m)
        if round is not None:
            mask_xyz = np.round(mask_xyz, round)
        mask_v_all.append(mask_v)
        mask_xyz_all.append(mask_xyz[:, (mask_v == 1).flatten()])

        if voxel_xyz.shape != mask_xyz.shape or not (voxel_xyz == mask_xyz).all():
            voxel_consistency = False

    # Get ROI flags
    if voxel_consistency:
        roi_flag = np.vstack(mask_v_all)
    else:
        roi_flag = get_roiflag(mask_xyz_all, voxel_xyz, verbose=verbose)

    # Add the ROI flag as metadata in `bdata`
    md_keys = []
    md_descs = []

    for i, roi in enumerate(roi_mask):
        roi_name = roi_prefix + '_' + os.path.basename(roi).replace('.nii.gz', '').replace('.nii', '').replace('-', '_')

        with open(roi, 'rb') as f:
            roi_md5 = hashlib.md5(f.read()).hexdigest()

        roi_desc = '1 = ROI %s (source file: %s; md5: %s)' % (roi_name, roi, roi_md5)
        if verbose:
            print('Adding %s' % roi_name)
            print('  %s' % roi_desc)
        md_keys.append(roi_name)
        md_descs.append(roi_desc)

    bdata.metadata.key.extend(md_keys)
    bdata.metadata.description.extend(md_descs)

    brain_data_index = bdata.get_metadata(brain_data)
    new_md_v = np.zeros([roi_flag.shape[0], bdata.metadata.value.shape[1]])
    new_md_v[:, :] = np.nan
    new_md_v[:, brain_data_index == 1] = roi_flag

    bdata.metadata.value = np.vstack([bdata.metadata.value, new_md_v])

    if return_roi_flag:
        return bdata, roi_flag
    else:
        return bdata

if __name__ == '__main__':
    # UKB
    subject_id = '5446423'

    data_loc, roi_loc, task_loc = get_data_locations(subject_id)
    opts = dict()
    opts['shift_size'] = 5
    opts['normalize_mode'] = 'PercentSignalChange'
    opts['voxel_coordinate_rounding'] = 3

    brain_data = make_dataset(data_loc, roi_loc, task_loc, opts)
    brain_data.show_metadata()

