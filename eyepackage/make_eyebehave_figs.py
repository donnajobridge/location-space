import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})

def edit_eye_variables(sub_fix_all_phase):
    roi_list = ['loc1start', 'loc2start', 'loc3start', 'screen']
    fig_roi_list = ['Original', 'Updated', 'Lure', 'Screen']
    cond_list = [1,2]
    fig_cond_list = ['Mismatch', 'Match']
    eye_measure_list = ['roi_num_mean', 'roi_dur_mean', 'roi_prop_mean']
    fig_eye_measure_list = ['Number of Fixations', 'Fixation Duration', 'Proportion of Viewing']
    recog_list = [1,2,3]
    fig_recog_list = ['Original', 'Updated', 'Lure']

    roi_dict = dict(zip(roi_list, fig_roi_list))
    cond_dict = dict(zip(cond_list, fig_cond_list))
    eye_measure_dict = dict(zip(eye_measure_list, fig_eye_measure_list))
    recog_loc_dict = dict(zip(recog_list, fig_recog_list))

    sub_fix_all_phase['cond']=sub_fix_all_phase['cond'].map(cond_dict)
    sub_fix_all_phase['roi']=sub_fix_all_phase['roi'].map(roi_dict)
    sub_fix_all_phase['recog loc']=sub_fix_all_phase['recog loc'].map(recog_loc_dict)

    sub_fix_all_phase.rename(columns = eye_measure_dict, inplace=True)
    sub_fix_all_phase.rename(columns = {'recog loc':'Recognition Location'}, inplace=True)
    return sub_fix_all_phase

def make_ave_eye_figs(fix_for_figs, phase):
    for cond in ['Mismatch', 'Match']:
        data = fix_for_figs[(fix_for_figs['phase']==phase) &
        (fix_for_figs['cond']==cond)]
        for measure in ['Number of Fixations', 'Fixation Duration', 'Proportion of Viewing']:
            for fig_type, myplot in [('bar', sns.barplot)]:
                ax=myplot(x='roi', y=measure, hue='Recognition Location',
                data=data, palette="colorblind")
                ax.set_xlabel('Region of Interest', fontsize=20)
                ax.tick_params(labelsize=16)
                plt.legend(fontsize=12)
                plt.gca().legend().set_title('')
                ax.set_ylabel('Mean ' + measure, fontsize=20)
                plt.title(measure, fontsize=30)
                fig=ax.get_figure()
                fig.savefig('../figs/ls_fix_'+fig_type+phase+cond+measure+'.png')
                plt.clf()


def edit_behave_variables(recog_prop_tidy):
    cond_list = [1,2]
    fig_cond_list = ['Mismatch', 'Match']
    recog_list = [1,2,3]
    fig_recog_list = ['Original', 'Updated', 'Lure']

    cond_dict = dict(zip(cond_list, fig_cond_list))
    recog_loc_dict = dict(zip(recog_list, fig_recog_list))

    recog_prop_tidy['cond']=recog_prop_tidy['cond'].map(cond_dict)
    recog_prop_tidy['recog loc']=recog_prop_tidy['recog loc'].map(recog_loc_dict)
    col_dict = {'recog loc':'Location Selection', 'loc_prop':'Proportion of Responses',
    'cond':'Condition'}
    recog_prop_tidy.rename(columns = col_dict, inplace=True)
    return recog_prop_tidy

def make_behave_figs(behave_for_figs):
    for fig_type, myplot in [('swarm', sns.violinplot)]:
        ax=myplot(x='Location Selection', y='Proportion of Responses', hue='Condition',
        data=behave_for_figs, palette="colorblind")
        ax.set_xlabel('Location Selection', fontsize=20)
        ax.tick_params(labelsize=16)
        plt.legend(fontsize=12)
        plt.gca().legend().set_title('')
        ax.set_ylabel('Proportion of Responses', fontsize=20)
        plt.title('Recognition Performance', fontsize=30)
        fig=ax.get_figure()
        fig.savefig('../figs/ls_behave_'+fig_type+'.png')
        plt.clf()
