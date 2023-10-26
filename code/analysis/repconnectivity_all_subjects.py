from rsa import representational_connectivity
import numpy as np
import os
import sys
from svm_decoder_model import get_roi_list


subject = sys.argv[1]

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
model_construction['roi_list'].extend(get_roi_list(['aseg'], combine_LR=True))
with open('rdsa_rois.txt', 'r') as f:
    roi_list = f.readlines()
result_file = '/external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/rsa_shp_sex_emotion/{}/'.format(subject)
roi_list = [s.strip() for s in roi_list]
print(subject)
rsa_roi = dict()
for idx2, roi in enumerate(roi_list):
    roi = roi.strip()
    data = np.load(os.path.join(result_file, 'rsa_{}.npy'.format(roi)))
    rsa_roi[roi] = data

connectivity_matrix = representational_connectivity(rsa_roi, model_construction, subject, save=False)
save_location = '/external/rprshnas01/netdata_kcni/dflab/team/ma/ukb/imaging/rsa_shp_sex_emotion/connectivity/'
# os.makedirs(save_location, exist_ok=True)
connectivity_matrix.to_csv('{}/{}.csv'.format(save_location, subject))
