import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})

#read in data
sublist=['ec105', 'ec106', 'ec107', 'ec108']
phase='refresh'
roi_list=['loc1start', 'loc2start', 'loc3start', 'screen']

def read_data_for_figs(sublist, phase):

    all=pd.DataFrame()
    for sub in sublist:
        file='data/' + sub + phase + 'eyebehave.csv'
        print(file)
        eye=pd.read_csv(file, index_col=0)
        all=pd.concat([all,eye])
    return all

def get_fixations(all):
    roimask=all['startloc']=='offscreen'
    all_roi=all[~roimask]
    all_fix=all_roi[all_roi['event']=='EFIX']
    all_fix=all_fix[all_fix['duration']>80]
    all_fix=all_fix[all_fix['recog loc']>0]
    return all_fix

def get_prop_tidy_prop_viewing(fix, roi_list):
    roi_prop_dict={}
    roi_prop_list=[]
    for row, ldf in fix.groupby(['sub', 'trialnum', 'cond', 'recog loc']):
        roi_sum = ldf['duration'].sum()
        for roi in rois:
            loc_ldf = ldf[ldf['startloc']==roi]
            loc_dur = loc_ldf['duration'].sum()
            loc_prop = loc_dur/roi_sum
            roi_prop_dict = {'sub':ldf['sub'].iloc[0], 'cond':ldf['cond'].iloc[0], 'trial':ldf['trialnum'].iloc[0],
                             'recog loc':ldf['recog loc'].iloc[0],
                             'all_roi_sum':roi_sum, 'roi':roi, 'roi_sum':loc_dur, 'roi_prop':loc_prop}
            roi_prop_list.append(roi_prop_dict)
    roi_prop_tidy=pd.DataFrame(roi_prop_list)
    return roi_prop_tidy
