from svm_decoder_model import get_roi_list
from rsa import calculate_rdsa, representational_connectivity
import sys

subject = sys.argv[1]

opts = dict()
opts['shift_size'] = 5
opts['normalize_mode'] = 'PercentSignalChange'
opts['voxel_coordinate_rounding'] = 3
model_construction = dict()
model_construction['number_of_splits'] = 6
model_construction['rsa_type'] = 'shp_sex_emotion'
model_construction['roi_list'] = get_roi_list(['hcp180'], combine_LR=False, suffices=['_bilateral'])
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
print(subject)
rdsa_dict = calculate_rdsa(subject, opts, model_construction, save_model=False)
representational_connectivity(rdsa_dict, model_construction, subject, save=True)
