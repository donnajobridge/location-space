import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# load theta amplitude data here
data = pd.read_csv('../data/theta_ev30.csv')
colmask = data.columns.str.contains('chan_3')
data = data.loc[750:1250,:]

data = data.loc[:,colmask]
cols = data.columns.tolist()


data = data['chan_3ev__1']
data = data.reset_index()

fig = plt.figure(figsize=(10, 4))

x = data['index']
y = data['chan_3ev__1']

plt.axvline(x=1002)
ax1 = fig.add_subplot(1,1,1)
# ax2 = fig.add_subplot(4,1,2, aspect=1080/1920)
# ax3 = fig.add_subplot(4,1,3, aspect=1080/1920)
# ax4 = fig.add_subplot(4,1,4, aspect=1080/1920)


ax1.set_xlim(750, 1250)
ax1.set_ylim(-50, 50)
ax1.set_title('Brain activity linked to viewing original location')
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)


line, = ax1.plot([], [], 'k-', alpha=0.5)
dot, = ax1.plot([], [], 'ko', alpha=.5)

def update_line(num, x,y, line, dot):
    line.set_data(x[:num], y[:num])
    dot.set_data(x[num-1:num], y[num-1:num])
    return line, dot,


line_ani = animation.FuncAnimation(fig, update_line, len(data), fargs=(x,y, line, dot),
                                   interval=1, blit=True)
plt.show()
