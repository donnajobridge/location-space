from pathlib import *
import numpy as np
import pandas as pd
from eyepackage.eye_parse import *
from eyepackage.behave_parse import *
from eyepackage.behave_eye_converge import *

# subids=["ec105","ec106","ec107","ec108"]
subids=["ec107","ec108"]
pathstring='/Volumes/Voss_Lab/ECOG/ecog/locationspace/ecog.eye/'
eyepath=Path(pathstring)

masternames=get_eye_files(subids,eyepath)
study_all=masternames[masternames['phase']=="a"]
refresh_all=masternames[masternames['phase']=="b"]
recog_all=masternames[masternames['phase']=="c"]

for sub in subids:
    refresh_sub=[]
    refresh_sub=refresh_all[refresh_all['subject']==sub]

    """ make everything below into a big subject loop"""
    '''read in eye data'''
    eye_events=parse_eye_line(refresh_sub,pathstring)
    eyedf=events_to_df(eye_events)
    eyearray=eventsdf_cleanup(eyedf)

    '''read in behavior'''
    behavestring='/Volumes/Voss_Lab/ECOG/ecog/locationspace/ecog.behave/'
    extra='recogarray.txt'
    behaveobj=[behavestring+sub+extra]
    behavepath=Path(behaveobj[0])
    behavepath.exists()
    behavearray=read_behave_file(behavepath)

    subdict_change_coords=change_behave_coords(subids)
    #apply coordinate change to behavioral data if True in subdict
    if subdict_change_coords[sub]==True:
        behavearray=apply_adjust_pres_coords(behavearray)

    '''read in object onset times'''
    reftimesextra='refreshtimes.txt'
    reftimesobj=[behavestring+sub+reftimesextra]
    reftimespath=Path(reftimesobj[0])
    reftimespath.exists()
    reftimes=read_times_file(reftimespath)

    ''' link behavior and eye data'''
    eyebehave=eye_behave_combo(eyearray,behavearray,reftimes)

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
    fname=sub+'eyebehave.csv'
    subcleandf.to_csv(fname)
