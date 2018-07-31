from pathlib import *
import numpy as np
import pandas as pd
from eyepackage.eye_parse import *
from eyepackage.behave_parse import *
from eyepackage.behave_eye_converge import *

def set_behavior_path(sub, behavestring):
    extra='recogarray.txt'
    behaveobj=[behavestring+sub+extra]
    behavepath=Path(behaveobj[0])
    behavepath.exists()
    return behavepath

def set_times_path(sub, behavestring, phase):
    timesarrayextra=phase+'times.txt'
    timesarrayobj=[behavestring+sub+timesarrayextra]
    timesarray_path=Path(timesarrayobj[0])
    timesarray_path.exists()
    return timesarray_path


def get_all_eye_files(subids,eyestring,phase):
    eyepath=Path(eyestring)
    if not eyepath.exists():
        print("can't find path, check connection!!")
        quit()
    phase_letter_dict={'study':'a', 'refresh':'b', 'recog':'c'}
    masternames=get_eye_files(subids,eyepath)
    phase_eye_files=masternames[masternames['phase_letter']==phase_letter_dict[phase]]
    print(phase_eye_files)
    return phase_eye_files

def load_data_for_subject(sub, phase_eye_files, phase, eyestring, behavestring, is_pres=True):
    eye_phase_sub=[]
    eye_phase_sub=phase_eye_files[phase_eye_files['subject']==sub]
    print(sub)
    eyearray = read_in_eye_data(eye_phase_sub,eyestring,phase)
    if not len(eyearray):
        print('eyearray is empty!')


    behavepath = set_behavior_path(sub, behavestring)
    timesarray_path = set_times_path(sub, behavestring, phase)

    behavearray=read_behave_file(behavepath)
    print('len(behavearray)', len(behavearray))
    #apply coordinate change to behavioral data if True in subdict
    if is_pres:
        behavearray=apply_adjust_pres_coords(behavearray)
        timesarray=read_times_file_pres(timesarray_path)
    else:
        timesarray=read_times_file_mat(timesarray_path,phase)

    print('len(timesarray)', len(timesarray))

    return eyearray,behavearray,timesarray

def preprocess_subject_dfs(sub,phase,eyearray,behavearray,timesarray):
    ''' link behavior and eye data'''
    eyebehave=eye_behave_combo(eyearray,behavearray,timesarray,phase)

    #adjust timing to object onset
    eyebehave=remove_baseline_eye(eyebehave)

    # calculate distances for start and end eye locations
    startdistarray=calculate_dist(eyebehave,x1='xstart',y1='ystart',name='start')
    enddistarray=calculate_dist(eyebehave,'xend','yend','end')

    # start & end locations
    eyebehave=loc_view(eyebehave,startdistarray,'startloc')
    eyebehave=loc_view(eyebehave,enddistarray,'endloc')

    #append start & end distances to eyebehave array
    eyebehave=pd.concat([eyebehave, startdistarray, enddistarray], axis=1)

    ''' change df to dict'''
    eyebehavedict=eyebehave.to_dict('records')
    ''' determine if non-loc viewing was on screen or offscreen'''
    eyebehavedict=assign_screenview(eyebehavedict,'xstart','ystart','start')
    eyebehavedict=assign_screenview(eyebehavedict,'xend','yend','end')

    '''adjust artifacts in eye data due to blinks'''
    new_previous_events=adjust_fix_before_blink(eyebehavedict)
    corrected_eye_events=adjust_event_after_blink(new_previous_events)

    '''put data back in df and remove old blinks'''
    subcleandf=eyedict_backto_df(corrected_eye_events)

    '''save subject specific file to csv'''
    # put that command in behave_eye_converge
    fname='data/'+sub+phase+'eyebehave.csv'
    subcleandf.to_csv(fname)

    bname='data/'+sub+'behave.csv'
    behavearray.to_csv(bname)
def run_all():
    subids=["ec109"]
    # subids=["ec105","ec106","ec107","ec108","ec109"]
    matlab_subs = ["ec105", "ec106"]
    pathstring='/Volumes/Voss_Lab/ECOG/ecog/locationspace/ecog.eye/'
    behavestring='/Volumes/Voss_Lab/ECOG/ecog/locationspace/ecog.behave/'



    for phase in ['study', 'refresh', 'recog']:

        all_phase = get_all_eye_files(subids,pathstring,phase)

        for sub in subids:
            is_pres = (sub not in matlab_subs)
            print('running', sub, 'using presentation', is_pres)
            output=load_data_for_subject(sub, all_phase, phase, pathstring, behavestring, is_pres)
            preprocess_subject_dfs(sub, phase, *output)
            print(sub, 'is done!')
