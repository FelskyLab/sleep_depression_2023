from nibabel.freesurfer.io import write_morph_data
import numpy as np
import pandas as pd
from os import path
import re

# from visbrain.objects import BrainObj , ColorbarObj, SceneObj, SourceObj

def roi_based_to_brain_map(roi_data_in_order, paradigm, filename, parcellation='dsk'):
    roi_info_location = '/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/{}'.format(parcellation)
    lh_labels = pd.read_csv(path.join(roi_info_location, 'label_lh.csv'), header=None)
    rh_labels = pd.read_csv(path.join(roi_info_location, 'label_rh.csv'), header=None)
    lh_label_codes = pd.read_csv(path.join(roi_info_location, 'label_codes_lh.csv'), header=None)
    rh_label_codes = pd.read_csv(path.join(roi_info_location, 'label_codes_rh.csv'), header=None)
    number_of_faces_fsaverage = 327680
    brain_map_lh = np.zeros(lh_labels.shape) - 99.0
    brain_map_rh = np.zeros(rh_labels.shape) - 99.0

    roi_data_lh = roi_data_in_order[0]
    roi_data_rh = roi_data_in_order[1]

    filename_lh = './results/' + paradigm + '/lh_' + filename
    filename_rh = './results/' + paradigm + '/rh_' + filename

    for lh_roi, lh_data in zip(lh_label_codes.values, roi_data_lh):
        brain_map_lh[lh_labels == lh_roi] = lh_data
    for rh_roi, rh_data in zip(rh_label_codes.values, roi_data_rh):
        brain_map_rh[rh_labels == rh_roi] = rh_data

    write_morph_data(filename_lh, brain_map_lh, number_of_faces_fsaverage)
    write_morph_data(filename_rh, brain_map_rh, number_of_faces_fsaverage)

def show_roi_order(hemisphere, parcellation='dsk'):
    roi_info_location = '/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/{}'.format(
        parcellation)
    roi_names = pd.read_csv(path.join(roi_info_location, 'roi_names_{}.csv'.format(hemisphere)))
    for idx, roi in enumerate(roi_names.values):
        print(idx, roi[0])

def reorder_to_roi_order(input_data, hemisphere, hemisphere_pattern, parcellation='dsk'):
    roi_info_location = '/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/{}'.format(
        parcellation)
    roi_names = pd.read_csv(path.join(roi_info_location, 'roi_names_{}.csv'.format(hemisphere)))
    roi_names_input = input_data.index
    reordered_data = pd.DataFrame(index=list(roi_names['roi_names'].values))
    for idx_target, roi_target in enumerate(roi_names.values):
        for idx_source, roi_source in enumerate(roi_names_input):
            input_to_regex = roi_target[0]
            if (hemisphere_pattern is None) & (parcellation == 'hcp180'):
                input_to_regex = input_to_regex[2:]
            input_to_regex = input_to_regex.replace('?', '\?')

            matching_pattern = re.findall('(^|_| |\n){}(_| |\n|$)'.format(input_to_regex), roi_source)
            if len(matching_pattern) > 0:
                if hemisphere_pattern is not None:
                    matching_hemisphere = re.findall('(^|_| |\n){}(_| |\n|$)'.format(hemisphere_pattern), roi_source)
                    if len(matching_hemisphere) > 0:
                        reordered_data.loc[roi_target[0], input_data.columns] = input_data.loc[roi_source][0]
                else:
                    reordered_data.loc[roi_target[0], input_data.columns] = input_data.loc[roi_source][0]
    # reordered_data.fillna(-99.0, inplace=True)
    return reordered_data

def reorder_to_custom_order(input_data, target_roi_names):
    roi_names_input = input_data.index
    reordered_data = pd.DataFrame(index=list(target_roi_names.values))
    for idx_target, roi_target in enumerate(target_roi_names.values):
        for idx_source, roi_source in enumerate(roi_names_input):
            input_to_regex = roi_target
            input_to_regex = input_to_regex.replace('?', '\?')

            matching_pattern = re.findall('(^|_| |\n){}(_| |\n|$)'.format(input_to_regex), roi_source)
            if len(matching_pattern) > 0:
                reordered_data.loc[roi_target, input_data.columns] = input_data.loc[roi_source][0]
    # reordered_data.fillna(-99.0, inplace=True)
    return reordered_data

def create_animated_roi_brain_map(data_functional, hemisphere='right', parcellation='dsk', title='', cblabel='corrlation', save=False):
    # Scene creation
    sc = SceneObj(bgcolor='black', size=(1400, 1000))
    # Colorbar default arguments. See `visbrain.objects.ColorbarObj`
    CBAR_STATE = dict(cbtxtsz=12, txtsz=10., width=.1, cbtxtsh=3.,
                      rect=(-.3, -2., 1., 4.))
    KW = dict(title_size=14., zoom=1.2)

    # Specify the parcellation file location
    parcellation_folder = '/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/fsaverage/label'
    if parcellation == 'dsk':
        path_to_file2 = '{}/{}h.aparc.annot'.format(parcellation_folder, hemisphere[0])
    elif parcellation == 'hcp180':
        path_to_file2 = '{}/{}h.HCP-MMP1.annot'.format(parcellation_folder, hemisphere[0])
    # Define the brain object (again... I know, this is redundant)
    b_obj_parr = BrainObj('inflated', hemisphere=hemisphere, translucent=False, sulcus=True)
    # Print parcellates included in the file
    parcellation_ctab = b_obj_parr.get_parcellates(path_to_file2)
    data_functional.index = parcellation_ctab['Labels']
    # From the list of printed parcellates, we only select a few of them
    select_par = list(data_functional.index[(data_functional.values != -99).squeeze()])
    # Now we define some data for each parcellates (one value per pacellate)
    data_par = data_functional.values[(data_functional.values != -99).squeeze()].reshape(-1)
    # Parcellize the brain with the selected parcellates. The data range is
    # between [.1, 11.]. Then, we use `vmin` and `vmax` to specify that we want
    # every parcellates under vmin to be gray and every parcellates over vmax
    # darkred
    b_obj_parr.parcellize(path_to_file2, select=select_par, hemisphere=hemisphere,
                          cmap='viridis', data=data_par)
    b_obj_parr.animate(iterations=-1, step=1., interval='auto')

    # Add the brain object to the scene
    sc.add_to_subplot(b_obj_parr, row=0, col=1, rotate='right',
                      title=title, **KW)
    # Get the colorbar of the brain object and add it to the scene
    cb_parr = ColorbarObj(b_obj_parr, cblabel=cblabel, **CBAR_STATE)
    sc.add_to_subplot(cb_parr, row=0, col=0, width_max=200)

    # sc.screenshot('ex_brain_obj.png', transparent=True, dpi=300, print_size=(10, 10), autocrop=True)
    if save:
        sc.record_animation('results/animate_example.gif', n_pic=100)
    else:
        sc.preview()




if __name__ == '__main__':
    lh_data_dummy = np.linspace(-5.0, 5.0, 181)
    rh_data_dummy = np.linspace(-3.0, 2.0, 181)
    filename='test_hcp180'
    test_data = pd.read_csv('test_data.csv', index_col='var')
    show_roi_order(hemisphere='lh', parcellation='dsk')
    reordered_custom = reorder_to_custom_order(test_data, pd.Series(data=['superiorfrontal', 'temporalpole', 'middletemporal']))
    reordered_lh = reorder_to_roi_order(test_data, 'lh', '\(left hemisphere\)', parcellation='dsk')
    reordered_rh = reorder_to_roi_order(test_data, 'rh', '\(right hemisphere\)', parcellation='dsk')
    # create_animated_roi_brain_map(reordered_rh, title='', cblabel='corrlation', save=False)
    roi_based_to_brain_map([reordered_lh.values, reordered_rh.values], filename, parcellation='dsk')
