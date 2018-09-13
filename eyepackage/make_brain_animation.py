import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def make_thetawave_gif(sub,trialnum):
    # Set up formatting for the movie files
    Writer = animation.writers['imagemagick']
    writer = Writer(fps=50, metadata=dict(artist='Me'), bitrate=1800)


    # load theta amplitude data here
    trial = str(trialnum)
    filestring = f'../raw_ieeg_data/{sub}_5hz_ev{trial}.csv'

    data = pd.read_csv(filestring)
    colmask = data.columns.str.contains('chan_3')

    data = data.loc[:,colmask]
    data = data.loc[750:1250,:]
    cols = data.columns.tolist()

    x = data.index
    ys = []
    for num,item in enumerate(data.columns.tolist()):
        y = f'y{num}'
        ys.append(data[item])

    def update_line(num, x,y, line, dot):
        line.set_data(x[:num], y[:num])
        dot.set_data(x[num-1:num], y[num-1:num])
        return line, dot,

    fig, axs = plt.subplots(nrows=data.shape[1], sharex=True, sharey=True, ncols=1,figsize=(10,10))
    plt.xlabel('Time (ms)')

    lines = []
    dots = []
    for ax in axs.flat:
        ax.axvline(x=1001)
        ax.set_xlim(750, 1250)
        ax.set_ylim(-40, 40)
        ax.set_xticks([750, 875, 1001, 1125, 1250])
        ax.set_xticklabels(['-500', '-250', '0', '250', '500'])
        ax.set_ylabel('Amplitude (mV)')
        ax.axvspan(825, 975, facecolor='b', alpha=0.1)
        line, = ax.plot([], [], 'k-', alpha=0.5)
        dot, = ax.plot([], [], 'ko', alpha=.5)

        lines.append(line)
        dots.append(dot)



    def update_lines(num, x, ys, lines, dots):
        out = ()
        for y, line, dot in zip(ys, lines, dots):
            tmpout = update_line(num, x=x, y=y, line=line, dot=dot)
            out = out + tmpout
        return out

    line_ani = animation.FuncAnimation(fig, update_lines, len(data),
                                       fargs=(x, ys, lines, dots), interval=1, blit=True)
    plt.tight_layout()
    plt.show()
    line_ani.save('../figs/theta_' + sub + '_reftr'+ trial + '_50fps.gif', writer=writer)

make_thetawave_gif('ec108',30)
print('finished gif')
make_thetawave_gif('ec108',74)
print('finished gif')
