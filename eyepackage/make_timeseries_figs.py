import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})


def make_lineplot(array, loclist, locnames, colorlist, phase, cond, accuracy):
    fig, ax = plt.subplots()
    for loc, label, color in zip(loclist, locnames, colorlist):
        line=sns.lineplot(data = array, x=array.index, y=loc, ax=ax,
        label=label, color=color)
        ax.legend(fontsize=16)
        ax.set_xlabel('Time (ms)', fontsize=24)
        ax.tick_params(labelsize=16)
        ax.set_xlim([0, 5000])
        ax.set_ylabel('Proportion of Viewing', fontsize=24)
        phasecap = phase.capitalize()
        plt.title(cond + ' ' + phasecap + ' ' + accuracy, fontsize=30)

    line=line.get_figure()
    line.savefig('../figs/line' + cond + phase + accuracy + '.png')
    # line.savefig('../figs/line' + trialtype + phase + '.eps', format='eps', dpi=1000)

    plt.clf()
