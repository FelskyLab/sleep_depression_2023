from glob import glob
from os import path
import pandas as pd
from builtins import range
from collections import OrderedDict
from pathlib import Path
import numpy as np
from tqdm import tqdm

def _text_to_df(text_file):
    """
    Convert a raw E-Prime output text file into a pandas DataFrame.
    """
    # Load the text file as a list.
    with open(text_file, 'rb') as fo:
        text_data = list(fo)

    # Remove unicode characters.
    filtered_data = [remove_unicode(row.decode('utf-8', 'ignore')) for row in text_data]

    # Determine where rows begin and end.
    start_index = [i for i, row in enumerate(filtered_data) if row == '*** LogFrame Start ***']
    end_index = [i for i, row in enumerate(filtered_data) if row == '*** LogFrame End ***']
    if len(start_index) != len(end_index) or start_index[0] >= end_index[0]:
        print('Warning: LogFrame Starts and Ends do not match up.',
              'Including header metadata just in case.')
        # In cases of an experiment crash, the final LogFrame is never written, and the experiment metadata
        # (Subject, VersionNumber, etc.) isn't collected by the indices above. We can manually include the
        # metadata-containing Header Frame to collect these data from a partial-run crash dump.
        start_index = [i for i,row in enumerate(filtered_data) if row == '*** Header Start ***'] + start_index
        end_index = [i for i,row in enumerate(filtered_data) if row == '*** Header End ***'] + end_index
    n_rows = min(len(start_index), len(end_index))

    # Find column headers and remove duplicates.
    headers = []
    data_by_rows = []
    for i in range(n_rows):
        one_row = filtered_data[start_index[i]+1:end_index[i]]
        data_by_rows.append(one_row)
        for col_val in one_row:
            split_header_idx = col_val.index(':')
            headers.append(col_val[:split_header_idx])

    headers = list(OrderedDict.fromkeys(headers))

    # Preallocate list of lists composed of NULLs.
    data_matrix = np.empty((n_rows, len(headers)), dtype=object)
    data_matrix[:] = np.nan

    # Fill list of lists with relevant data from data_by_rows and headers.
    for i in range(n_rows):
        for cell_data in data_by_rows[i]:
            split_header_idx = cell_data.index(':')
            for k_header, header in enumerate(headers):
                if cell_data[:split_header_idx] == header:
                    data_matrix[i, k_header] = cell_data[split_header_idx+1:].lstrip()

    df = pd.DataFrame(columns=headers, data=data_matrix)

    # Columns with one value at the beginning, the end, or end - 1 should be
    # filled with that value.
    for col in df.columns:
        non_nan_idx = np.where(df[col].values == df[col].values)[0]
        if len(non_nan_idx) == 1 and non_nan_idx[0] in [0, df.shape[0]-1,
                                                        df.shape[0]-2]:
            df.loc[:, col] = df.loc[non_nan_idx[0], col]
    return df

def remove_unicode(string):
    """
    Removes unicode characters in string.
    Parameters
    ----------
    string : str
        String from which to remove unicode characters.
    Returns
    -------
    str
        Input string, minus unicode characters.
    """
    return ''.join([val for val in string if 31 < ord(val) < 127])

if __name__ == '__main__':
    data_location = '../../data/task/behavior'
    xml_files_folder = 'raw'
    output_files_folder = 'csv'
    number_of_volumes = np.loadtxt('../../data/fMRI_volume_allocation.csv', delimiter=',')

    valid_files = list()
    xml_files = glob(path.join(data_location, xml_files_folder,'*.txt'))
    xml_files_loop = tqdm(xml_files)
    for idx, xml_file in enumerate(xml_files_loop):
        xml_files_loop.set_postfix_str('File: {}'.format(Path(xml_file).stem))
        try:
            data = _text_to_df(xml_file)
        except:
            continue
        if data.shape[0] < 75:
            continue
        valid_files.append(Path(xml_file).stem)
        if path.isfile(path.join(data_location, output_files_folder,'{}.csv'.format(Path(xml_file).stem))):
            continue

        experiment_timing = pd.DataFrame(columns=['label', 'image_top', 'image_left', 'image_right', 'emotion',
                                                  'response', 'correct_response', 'accuracy', 'response_time',
                                                  'number_of_fmri_volumes'])

        experiment_timing['image_top'] = data['Top'] #image appearing on the top position in experiment
        experiment_timing['image_left'] = data['Left']  #image appearing on the left position in experiment
        experiment_timing['image_right'] = data['Right'] #image appearing on the right position in experiment
        experiment_timing['response'] = data['StimSlide.RESP'] #the response the subject gave
        experiment_timing['correct_response'] = data['StimSlide.CRESP'] #the correct response
        experiment_timing['accuracy'] = data['StimSlide.ACC'] #accuracy of response (0 or 1)
        experiment_timing['response_time'] = data['StimSlide.RT'] # response time
        #Face vs Shape vs Rest
        experiment_timing['label'] = data['Procedure']
        for idx in np.arange(1, 7):
            experiment_timing['label'].loc[np.where(experiment_timing['label'] == 'ShapePromptPROC')[0] + idx] = 'ShapeTrialPROC'
            experiment_timing['label'].loc[np.where(experiment_timing['label'] == 'FacePromptPROC')[0] + idx] = 'FaceTrialPROC'
        # Fear vs. Anger
        experiment_timing['emotion'] = data['Top']
        experiment_timing['emotion'].fillna('Non-face', inplace=True)
        experiment_timing['emotion'].loc[experiment_timing['emotion'].str.match('^(M|F)A.+')] = 'anger'
        experiment_timing['emotion'].loc[experiment_timing['emotion'].str.match('^(M|F)F.+')] = 'fear'
        experiment_timing['emotion'].loc[experiment_timing['emotion'].str.match('^oval.+')] = 'Non-face'
        experiment_timing['emotion'].loc[experiment_timing['emotion'].str.match('^circle.+')] = 'Non-face'
        experiment_timing.drop(74, inplace=True)
        experiment_timing['number_of_fmri_volumes'] = number_of_volumes
    #   data.info()
        experiment_timing.to_csv(path.join(data_location, output_files_folder,'{}.csv'.format(Path(xml_file).stem)))
    print('Number of valid files = {}'.format(len(valid_files)))
