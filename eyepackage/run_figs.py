import numpy as np
import pandas as pd
from eyepackage.organize_eyebehave_for_figs import *
from eyepackage.make_eyebehave_figs import *

def run_all_figs():
    sublist = ['ec105', 'ec106', 'ec107', 'ec108', 'ec109']
    phaselist = ['study','refresh','recog']
    roi_list = ['loc1start', 'loc2start', 'loc3start', 'screen']
    fig_roi_list = ['Original', 'Updated', 'Lure', 'Screen']
    cond_list = [1,2]
    fig_cond_list = ['Mismatch', 'Match']


    sub_fix_all_phase = pd.DataFrame()
    phase_data_dict = {}
    for phase in phaselist:
        all_eye_events = read_eye_data(sublist, phase)
        fix = get_fixations(all_eye_events)
        roi_fix_tidy = get_tidy_fix(fix, roi_list)
        sub_fix_tidy = get_tidy_fix_sub(roi_fix_tidy)
        sub_fix_tidy['phase'] = phase
        fix_for_figs = edit_eye_variables(sub_fix_tidy)
        phase_data_dict[phase] = fix_for_figs

    for phase in phaselist:
        fig_data = phase_data_dict[phase]
        make_bar_ave_eye(fig_data, phase)
        make_vio_ave_eye(fig_data, phase)
        # todo: add eye fig functions



    all_behave = read_behave_data(sublist)
    recog_prop_tidy = get_tidy_prop_recog(all_behave)

    behave_for_figs = edit_behave_variables(recog_prop_tidy)
    make_bar_behave(behave_for_figs)
    make_vio_behave(behave_for_figs)
