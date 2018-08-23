import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def make_timeseries(eyearray, condnum, phase):
    trialorder = phase + ' order'
    eyearray[['start', 'end', trialorder]] = eyearray[['start', 'end', trialorder]].astype(int)
    alltimearray = pd.DataFrame(index=range(5500), columns=range(0,129))
    cortimearray = pd.DataFrame(index=range(5500), columns=range(0,129))
    fix = eyearray[(eyearray['event']=='EFIX') & (eyearray['cond']==condnum)]
    offmask = (fix['startloc'] == 'offscreen')
    fix.loc[offmask, 'startloc'] = np.nan

    for trial, ldf in fix.groupby(by=[trialorder]):

        for item, trialinfo in ldf.iterrows():
            start = trialinfo['start']
            end = trialinfo['end']
            loc = trialinfo['startloc']
            accuracy = (trialinfo['recog loc'] == 1)

            alltimearray.iloc[start:end, trial] = loc

            if not accuracy:
                continue
            cortimearray.iloc[start:end, trial] = loc

    alltimearray.dropna(axis=1, how='all', inplace = True)
    cortimearray.dropna(axis=1, how='all', inplace = True)
    return alltimearray, cortimearray

def get_timeseries_props(timearray, sub):
    numtrials = timearray.shape[1]
    props = pd.DataFrame(index=range(timearray.shape[0]))
    alltot = timearray.count(axis=1)
    props['total_fix'] = alltot
    objlist = ['loc1start', 'loc2start', 'loc3start', 'screen']

    for loc in objlist:
        objset = timearray[timearray==loc].count(axis=1)
        props[loc] = objset/alltot

    props.reset_index(inplace=True)
    props.rename(columns={'index':'time'}, inplace=True)
    props['sub'] = sub
    return props

def downsample_timeseries(timearray, newsamplerate):
    alltimes = timearray.time.unique()
    times_to_keep = alltimes[0:len(alltimes):newsamplerate]
    downsampled = timearray.set_index('time')
    downsampled = downsampled.loc[times_to_keep,:]
    return downsampled
