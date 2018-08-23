import pandas as pd
import numpy as np


#read in data

def read_eye_data(sublist, phase):
    all=pd.DataFrame()
    for sub in sublist:
        file='../data/' + sub + phase + 'eyebehave.csv'
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

def get_tidy_fix(fix, roi_list):
    roi_prop_dict={}
    roi_prop_list=[]
    for row, ldf in fix.groupby(['sub', 'trialnum', 'cond', 'recog loc']):
        roi_sum = ldf['duration'].sum()
        for roi in roi_list:
            loc_ldf = ldf[ldf['startloc']==roi]
            loc_dur = loc_ldf['duration'].sum()
            loc_prop = loc_dur/roi_sum
            roi_prop_dict = {'sub':ldf['sub'].iloc[0], 'cond':ldf['cond'].iloc[0], 'trial':ldf['trialnum'].iloc[0], 'recog loc':ldf['recog loc'].iloc[0],'all_roi_dur':roi_sum, 'roi':roi, 'roi_dur':loc_dur,'roi_prop':loc_prop, 'roi_num':loc_ldf.shape[0]}
            roi_prop_list.append(roi_prop_dict)
    roi_fix_tidy=pd.DataFrame(roi_prop_list)
    return roi_fix_tidy


def get_tidy_fix_sub(roi_fix_tidy):
    sub_fix_list = []
    for row, ldf in roi_fix_tidy.groupby(['sub', 'cond', 'roi', 'recog loc']):
        roi_num_mean=ldf['roi_num'].mean()
        roi_dur_mean=ldf['roi_dur'].mean()
        roi_prop_mean=ldf['roi_prop'].mean()
        sub_fix_dict = {'sub':row[0], 'cond':row[1], 'roi':row[2], 'recog loc':row[3],
                       'roi_num_mean':roi_num_mean, 'roi_dur_mean':roi_dur_mean, 'roi_prop_mean':roi_prop_mean}
        sub_fix_list.append(sub_fix_dict)
    sub_fix_tidy=pd.DataFrame(sub_fix_list)
    return sub_fix_tidy


def read_behave_data(sublist):
    all_behave=pd.DataFrame()
    for sub in sublist:
        file='../data/' + sub + 'behave.csv'
        behave=pd.read_csv(file, index_col=0)
        behave['sub']=sub
        all_behave=pd.concat([all_behave,behave])
    return all_behave

def get_tidy_prop_recog(all_behave):
    all_behave=all_behave[all_behave['recog loc']!=-1]
    locs=[1, 2, 3]
    recog_prop_dict={}
    recog_prop_list=[]
    for row, ldf in all_behave.groupby(['sub', 'cond']):
        for loc in locs:
            loc_ldf = ldf[ldf['recog loc']==loc]
            loc_prop = loc_ldf['recog loc'].count()/ldf.shape[0]
            recog_prop_dict = {'sub':row[0], 'cond':row[1], 'recog loc':loc, 'loc_prop':loc_prop}
            recog_prop_list.append(recog_prop_dict)
    recog_prop_tidy=pd.DataFrame(recog_prop_list)
    return recog_prop_tidy
