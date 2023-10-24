import os
from bdpy_make_dataset import add_roimask
from bdpy import BData
from bdpy.mri.load_mri import load_mri
from glob import glob
from bdpy.mri import get_roiflag
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.svm import SVC
import numpy as np
import pandas as pd
from svm_decoder_model import get_all_rois, get_roi_list
import sys

def extract_seed_based_correlation_results(subject_id, roi_list, seed_roi_name, bilateral=True, verbose=True):
    data_loc, roi_loc = get_data_locations(subject_id, seed_roi_name, roi_list)
    VoxelData, xyz, ijk = load_mri(data_loc)
    VoxelData = np.expand_dims(VoxelData, axis=0)

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

    for roi_location in roi_loc:
        roi_files = glob(os.path.join(roi_location, '*.nii.gz'))
        if bilateral:
            roi_files = list(set.difference(set(roi_files), set(glob(os.path.join(roi_location, '[R|L]_*.nii.gz')))))
        roi_group = roi_location.split(os.path.sep)[-3]
        for file in roi_files:
            bdata = add_roimask(bdata, file, roi_prefix='roi_{}'.format(roi_group), brain_data='VoxelData', verbose=verbose, round=3)

    return bdata

def get_data_locations(subject, seed_roi, roi_groups):
    base_location = '/external/rprshnas01/external_data/uk_biobank/imaging/brain/nifti/fmri_resting'
    data_location = '{}/data/{}_20227_2_0/seed_based_correlation/{}/dr_stage2_subject00000.nii.gz'.format(base_location, subject, seed_roi)
    roi_locations = list()
    for roi in roi_groups:
        roi_location = '{}/data_roi/{}/{}/'.format(base_location, roi, subject)
        roi_locations.append(roi_location)

    return data_location, roi_locations

def extract_mean_correlation(subject_id, roi_parcellations, options):
    roi_list_names = options['roi_list']
    connectivity_matrix = pd.DataFrame(index=roi_list_names, columns=roi_list_names)

    for seed_roi in roi_list_names:
        seed_roi_folder = seed_roi.split('_', 2)[-1]
        brain_data = extract_seed_based_correlation_results(subject_id, roi_parcellations, seed_roi_folder,
                                                            bilateral=options['bilateral'], verbose=False)
        for target_roi in roi_list_names:
            voxels = brain_data.select(target_roi)
            connectivity_matrix.loc[seed_roi, target_roi] = voxels.mean()

    return connectivity_matrix

def extract_mean_correlation_one_seed(subject_id, roi_parcellations, seed_roi, options):
    roi_list_names = options['roi_list']
    connectivity_matrix = pd.DataFrame(index=[seed_roi], columns=roi_list_names)

    brain_data = extract_seed_based_correlation_results(subject_id, roi_parcellations, seed_roi,
                                                        bilateral=options['bilateral'], verbose=False)
    for target_roi in roi_list_names:
        voxels = brain_data.select(target_roi)
        connectivity_matrix.loc[seed_roi, target_roi] = voxels.mean()

    return connectivity_matrix


if __name__ == '__main__':
    import time
    import resource

    start_time = time.time()
    subject = sys.argv[1]
    print(subject)
    rois_in_bdata = ['hcp180']
    opts = dict()
    opts['roi_list'] = get_roi_list(['hcp180'], combine_LR=False, suffices=['_bilateral'])
    opts['bilateral'] = True
    model_construction = dict()
    aggregated_results = pd.DataFrame(index=opts['roi_list'], columns=opts['roi_list'])
    results = extract_mean_correlation(subject, rois_in_bdata, opts)
    print("--- %s seconds elapsed ---" % (time.time() - start_time))
    # roi_list_data.extend(get_roi_list(['aseg'], combine_LR=True))
    # for roi in opts['roi_list']:
    #     roi_name = roi[11:]
    #
    #     aggregated_results.loc[roi, :] = results.loc[roi_name, :]

    print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)