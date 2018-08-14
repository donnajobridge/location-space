import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})


def make_lineplot(array, loclist, locnames, colorlist, phase, trialtype):
    fig, ax = plt.subplots()
    for loc, label, color in zip(loclist, locnames, colorlist):
        line=sns.lineplot(data = array, x=array.index, y=loc, ax=ax,
        label=label, color=color)
        ax.legend()
        ax.set_xlabel('Time (ms)')
        ax.set_xlim([0, 5000])
        ax.set_ylabel('Proportion of Viewing')
    line=line.get_figure()
    line.savefig('../figs/line' + trialtype + phase + '.png')
    plt.clf()
