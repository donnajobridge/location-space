import numpy as np
import pandas as pd
from get_timeseries import *
from make_timeseries_figs import *


sublist=['ec105', 'ec106', 'ec107', 'ec108', 'ec109']
loclist = ['loc1start', 'loc2start', 'loc3start']
locnames = ['Original', 'Updated', 'New']
shortloclist = ['loc1start', 'loc2start']
shortlocnames = ['Original', 'New']
phaselist=['refresh','recog']
condlist=["Mismatch", "Match"]
condnums=[1,2]

for cond, condnum in zip(condlist,condnums):
    for phase in phaselist:
        allprops = pd.DataFrame()
        corprops = pd.DataFrame()
        for sub in sublist:
            file='../data/' + sub + phase + 'eyebehave.csv'
            print(file)
            eye=pd.read_csv(file, index_col=0)

            alltimearray, cortimearray = make_timeseries(eye, condnum, phase)

            corprops_sub = get_timeseries_props(cortimearray, sub)
            allprops_sub = get_timeseries_props(alltimearray, sub)

            corprops_sub_down = downsample_timeseries(corprops_sub, 100)
            allprops_sub_down = downsample_timeseries(allprops_sub, 100)

            corprops = pd.concat([corprops, corprops_sub_down])
            allprops = pd.concat([allprops, allprops_sub_down])

        colorlist = ['darkorchid', 'mediumspringgreen', 'darkturquoise']
        shortcolorlist = ['mediumspringgreen', 'darkturquoise']

        make_lineplot(corprops, loclist, locnames, colorlist, phase, cond, 'Stability')
        make_lineplot(allprops, loclist, locnames, colorlist, phase, cond, 'All')
        # if cond != 1:
        #     break
        # if phase != 'refresh':
        #     break
        # make_lineplot(corprops, shortloclist, shortlocnames, shortcolorlist, phase, "Mismatch", 'Memory')
        corname='../data/cortrials'+phase+cond+'eyetimeseries.csv'
        corprops.to_csv(corname)
        allname='../data/alltrials'+phase+cond+'eyetimeseries.csv'
        allprops.to_csv(allname)
