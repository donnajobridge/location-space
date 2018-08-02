import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


rcParams.update({'figure.autolayout': True})


# to do: edit function for plotting eye movements across phases

sub='ec108'
subdf=all_eye_events[(all_eye_events['sub']==sub) & (all_eye_events['refresh order']==30) ]
print(subdf['cond'])
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(subdf.xstart, subdf.ystart, marker='.', alpha=0.3)
ax.plot(subdf.xstart, subdf.ystart, marker='.', alpha=0.3)
ax.scatter(subdf.loc1x, subdf.loc1y, marker='*', c='cyan')
ax.scatter(subdf.loc2x, subdf.loc2y, marker='*', c='red')
ax.scatter(subdf.loc3x, subdf.loc3y, marker='*', c='green')
plt.xlim(0, 1920)
plt.ylim(0, 1080)
# plt.savefig('figs/eye_path_ec108_tr30_recog.eps', format='eps', dpi=1000)
