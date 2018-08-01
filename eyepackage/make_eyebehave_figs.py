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

def make_bar_ave_eye(fix_for_figs, phase):
    for cond in ['Mismatch', 'Match']:
        data = fix_for_figs[(fix_for_figs['phase']==phase) &
        (fix_for_figs['cond']==cond)]
        for measure in ['Number of Fixations', 'Fixation Duration', 'Proportion of Viewing']:
            bar=sns.barplot(x='roi', y=measure, hue='Recognition Location', data=data, palette="colorblind")
            bar.set_xlabel('Region of Interest', fontsize=20)
            bar.tick_params(labelsize=16)
            plt.legend(fontsize=12)
            plt.gca().legend().set_title('')
            bar.set_ylabel('Mean ' + measure, fontsize=20)
            plt.title(measure, fontsize=30)
            barfig=bar.get_figure()
            barfig.savefig('figs/ls_fix_bar_'+phase+cond+measure+'.png')
            plt.clf()

def make_vio_ave_eye(fix_for_figs, phase):
    for cond in ['Mismatch', 'Match']:
        data = fix_for_figs[(fix_for_figs['phase']==phase) &
        (fix_for_figs['cond']==cond)]
        for measure in ['Number of Fixations', 'Fixation Duration', 'Proportion of Viewing']:
            vio=sns.violinplot(x='roi', y=measure, hue='Recognition Location', data=data, palette="colorblind")
            vio.set_xlabel('Region of Interest', fontsize=20)
            vio.tick_params(labelsize=16)
            plt.legend(fontsize=12)
            plt.gca().legend().set_title('')
            vio.set_ylabel('Mean ' + measure, fontsize=20)
            plt.title(measure, fontsize=30)
            viofig=vio.get_figure()
            viofig.savefig('figs/ls_fix_vio_'+phase+cond+measure+'.png')
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

def make_bar_behave(behave_for_figs):
    bar=sns.barplot(x='Location Selection', y='Proportion of Responses', hue='Condition',
    data=behave_for_figs, palette="colorblind")
    bar.set_xlabel('Location Selection', fontsize=20)
    bar.tick_params(labelsize=16)
    plt.legend(fontsize=12)
    plt.gca().legend().set_title('')
    bar.set_ylabel('Proportion of Responses', fontsize=20)
    plt.title('Recognition Performance', fontsize=30)
    barfig=bar.get_figure()
    barfig.savefig('figs/ls_behave_bar_.png')
    plt.clf()

def make_vio_behave(behave_for_figs):
    vio=sns.violinplot(x='Location Selection', y='Proportion of Responses', hue='Condition',
    data=behave_for_figs, split=True, inner='stick',  palette="colorblind")
    vio.set_xlabel('Location Selection', fontsize=20)
    vio.tick_params(labelsize=16)
    plt.legend(fontsize=12)
    plt.gca().legend().set_title('')
    vio.set_ylabel('Proportion of Responses', fontsize=20)
    plt.title('Recognition Performance', fontsize=30)
    viofig=vio.get_figure()
    viofig.savefig('figs/ls_behave_vio_.png')
    plt.clf()
