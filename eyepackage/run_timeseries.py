import numpy as np
import pandas as pd
from get_timeseries import *
from make_timeseries_figs import *


sublist=['ec105', 'ec106', 'ec107', 'ec108', 'ec109']
loclist = ['loc1start', 'loc2start', 'loc3start']
locnames = ['Original', 'Updated', 'New']
phase='refresh'

allprops = pd.DataFrame()
corprops = pd.DataFrame()

for sub in sublist:
    file='../data/' + sub + phase + 'eyebehave.csv'
    print(file)
    eye=pd.read_csv(file, index_col=0)

    alltimearray, cortimearray = make_timeseries(eye, 1, phase)

    corprops_sub = get_timeseries_props(cortimearray, sub)
    allprops_sub = get_timeseries_props(alltimearray, sub)

    corprops_sub_down = downsample_timeseries(corprops_sub, 100)
    allprops_sub_down = downsample_timeseries(allprops_sub, 100)

    corprops = pd.concat([corprops, corprops_sub_down])
    allprops = pd.concat([allprops, allprops_sub_down])

colorlist = ['darkorchid', 'mediumspringgreen', 'darkturquoise']

make_lineplot(corprops, loclist, locnames, colorlist, phase, 'stability')
make_lineplot(allprops, loclist, locnames, colorlist, phase, 'all')
