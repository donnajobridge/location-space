from pathlib import *
import numpy as np
import pandas as pd

def parse_eye_filename(pathobject):
    fname=pathobject.name
    parts=fname.split(".")[0]
    subject=parts[:5]
    other=parts[5:]
    has_r="r" in other
    if has_r:
        other=other.replace("r","")
    try:
        block=int(other[0])
        phase_letter=other[1]
    except:
        block=int(other[1])
        phase_letter=other[0]
    subdict={"subject":subject, "phase_letter":phase_letter,"block":block, "fname":fname}
    return subdict


def get_eye_files(subids,eyepath):
    """ returns master dataframe including eye file name, block, phase, subid
    input list of subject strings, Path object pointing to eye files
    """
    substrings=[s+"*.asc" for s in subids]
    subinfo=[]
    for s in substrings:
        for filepathobj in eyepath.glob(s):
            subdict=parse_eye_filename(filepathobj)
            subinfo.append(subdict)

    masterdf=pd.DataFrame(subinfo).sort_values(by=["subject","phase_letter","block"])
    masterdf=masterdf[["subject","phase_letter","block","fname"]]
    masterdf.index=range(len(masterdf))
    return masterdf


def parse_eye_events_to_intline(line,extrainfo):
    efixspace=["","",""]
    eblinkspace=efixspace*2
    newline=line.split()
    if "EFIX" in line:
        newline.extend(efixspace)
    elif "EBLINK" in line:
        newline.extend(eblinkspace)
    newline.extend(extrainfo)
    return newline


def parse_eye_line(eye_phase_sub,eyestring, phase):
    """ parses each line of eye file for a given eye_phase_sub
    input one phase type list of files for a subs
    and the path to the file (in form of a string)
    outputs dataframe with all events in table
    """
    etypes=('ESACC','EFIX','EBLINK')
    events=[]
    blocks=eye_phase_sub.block
    fnames=eye_phase_sub.fname
    subjects=eye_phase_sub.subject
    trialnum=0
    for block,fname,subject in zip(blocks,fnames,subjects):
        path_file=eyestring+fname
        startcount=0
        p=Path(path_file)
        with p.open() as f:
            for line in f:
                if "START" in line:
                    startcount=startcount+1
                    if phase=='study' and startcount==1:
                        trialnum=trialnum
                    else:
                        trialnum=trialnum+1
                    startline=line.split()
                    starttime=int(startline[1])
                if any(e in line for e in etypes):
                    extrainfo=[starttime,trialnum,block,subject]
                    newline=parse_eye_events_to_intline(line,extrainfo)
                    if phase=='study' and startcount==1:
                        continue
                    events.append(newline)
    return events

def events_to_df(events):
    """ change raw events to data DataFrame
    then and change values to numeric"""

    eye_events_df=pd.DataFrame(events)
    eye_events_df=eye_events_df.apply(pd.to_numeric,errors='ignore')
    headers=["event","eye","start","end","duration",
    "xstart","ystart","xend","yend","?","?","trialstart",
    "trialnum","block","sub"]
    eye_events_df.columns=headers
    return eye_events_df

def eventsdf_cleanup(eye_events_df):
    """adjust trial start time, remove irrelevant values in fixation rows,
    and then delete excess columns"""

    eyedf_clean=eye_events_df.copy()

    eyedf_clean['start']=eyedf_clean['start']-eyedf_clean['trialstart']
def eventsdf_cleanup(eye_events_df):
    """adjust trial start time, remove irrelevant values in fixation rows,
    and then delete excess columns"""

    eyedf_clean=eye_events_df.copy()

    eyedf_clean['start']=eyedf_clean['start']-eyedf_clean['trialstart']
    eyedf_clean['end']=eyedf_clean['end']-eyedf_clean['trialstart']

    efix_mask = (eyedf_clean["event"]=="EFIX")
    eyedf_clean.loc[efix_mask, 'xend'] = np.nan

    del eyedf_clean['trialstart']
    del eyedf_clean['?']
    del eyedf_clean['eye']

    return eyedf_clean

def read_in_eye_data(eye_phase_sub,eyestring,phase):
    eye_events=parse_eye_line(eye_phase_sub,eyestring,phase)
    eyedf=events_to_df(eye_events)
    eyearray=eventsdf_cleanup(eyedf)
    return eyearray
