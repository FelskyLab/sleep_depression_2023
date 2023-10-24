import pandas as pd
import numpy as np
from visbrain.objects import ConnectObj, SceneObj, SourceObj, BrainObj

def plot_connectivity_brain(indep_vars, measure='representational_connectivity', save=False):
    # create scene obj
    sc = SceneObj(size=(1500, 600), bgcolor='white')
    # Nodes
    hcp180_lh_nodes = pd.read_csv(
        '/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/freesurfer_label_info/hcp180/lh_vertex_means_pre.csv',
        index_col=0)
    hcp180_lh_nodes = hcp180_lh_nodes.values[1:, :]

    for idx, var in enumerate(indep_vars):
        p_values = np.load('{}_{}_p_values.npy'.format(measure, var))
        b_values = np.load('{}_{}_b_values.npy'.format(measure, var))
        b_values_corr = b_values.copy()
        b_values_corr[p_values > 0.05 / 5] = np.nan
        con_mat = b_values_corr
        ## # Define the connectivity and source objects
        c_cuscol = ConnectObj('default', hcp180_lh_nodes, con_mat, select=~np.isnan(con_mat),
                              color_by='strength', cmap='coolwarm', clim=[-.01, .01], alpha=0.2)
        s_obj_cu = SourceObj('sources', hcp180_lh_nodes, color='black', radius_min=2.,
                             symbol='ring', alpha=0.2)
        # Add objects to the scene
        sc.add_to_subplot(BrainObj('inflated_pre', translucent=True, hemisphere='left'), row=0, col=idx,
                          rotate='left')

        sc.add_to_subplot(c_cuscol, row=0, col=idx)
        sc.add_to_subplot(s_obj_cu, row=0, col=idx)

        # Finally, display the scene

    sc.screenshot(
        '/external/rprshnas01/kcni/mabdelhack/uk_biobank/tfmri/imaging/{}_brain_connect_rdsa_230217.png'.format(var),
        print_size=(5, 5), dpi=600, transparent=True)
    sc.preview()

if __name__ == '__main__':
    independent_vars = ['duration_of_longest_sleep_bout',
                        'Sleeplessness___insomnia',
                        'Number_of_symbol_digit_matches_made_correctly',
                        'phq2',
                        'Daytime_dozing___sleeping_narcolepsy']
    plot_connectivity_brain(independent_vars, measure='representational_connectivity')
    plot_connectivity_brain(independent_vars, measure='seed_based_correlation')

