import numpy as np
import matplotlib
import pandas as pd
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from imageio import imread

# Set up formatting for the movie files
Writer = animation.writers['imagemagick']
writer = Writer(fps=5, metadata=dict(artist='Me'), bitrate=1800)


sub='ec108'
phases=['study', 'refresh', 'recog']
ref_trial_num = 30

df_dict={}
for phase in phases:
    file='../data/' + sub + phase + 'eyebehave.csv'
    df_dict[phase]=pd.read_csv(file, index_col=0)


study_all = df_dict['study']
refresh_all = df_dict['refresh']
recog_all = df_dict['recog']

study = study_all[(study_all['sub']==sub) & (study_all['refresh order']==ref_trial_num) ]
refresh = refresh_all[(refresh_all['sub']==sub) & (refresh_all['refresh order']==ref_trial_num) ]
recog = recog_all[(recog_all['sub']==sub) & (recog_all['refresh order']==ref_trial_num) ]

apple = imread('../figs/apple.png')
grid = imread('../figs/grid.png')
apple2 = apple[::-1]


fig = plt.figure(figsize=(10, 4))

ax1 = fig.add_subplot(1,3,1, aspect=1080/1920)
ax2 = fig.add_subplot(1,3,2, aspect=1080/1920)
ax3 = fig.add_subplot(1,3,3, aspect=1080/1920)

ax1.set_xlim(0, 1920)
ax1.set_ylim(0, 1080)
ax1.set_title('Study', fontsize=20)
ax1.axes.get_xaxis().set_visible(False)
ax1.axes.get_yaxis().set_visible(False)

ax2.set_xlim(0, 1920)
ax2.set_ylim(0, 1080)
ax2.set_title('Mismatch', fontsize=20)
ax2.axes.get_xaxis().set_visible(False)
ax2.axes.get_yaxis().set_visible(False)

ax3.set_xlim(0, 1920)
ax3.set_ylim(0, 1080)
ax3.set_title('Recognition', fontsize=20)
ax3.axes.get_xaxis().set_visible(False)
ax3.axes.get_yaxis().set_visible(False)

offset = 180

# loc1 = {key: subdf[f'loc1{key}'].iloc[0] for key in ['x', 'y']}
# loc2 = {key: subdf[f'loc2{key}'].iloc[0] for key in ['x', 'y']}

# loc1_coords = [loc1['x']-offset, loc1['x']+offset, loc1['y']+offset, loc1['y']-offset]
# loc2_coords = [loc2['x']-offset, loc2['x']+offset, loc2['y']+offset, loc2['y']-offset]


# for plotting apple
def coords_to_borders(subdf, loc, offset):
    xi = subdf[f'loc{loc}x'].iloc[0]
    yi = subdf[f'loc{loc}y'].iloc[0]
    return [xi-offset, xi+offset, yi+offset, yi-offset]

loc1_coords = coords_to_borders(refresh, loc=1, offset=offset)
loc2_coords = coords_to_borders(refresh, loc=2, offset=offset)
loc3_coords = coords_to_borders(refresh, loc=3, offset=offset)

# plot grid
ax1.imshow(grid, extent = [0, 1920, 0, 1080])
ax2.imshow(grid, extent = [0, 1920, 0, 1080])
ax3.imshow(grid, extent = [0, 1920, 0, 1080])

#plot apple
# study
ax1.imshow(apple2, extent = loc1_coords)
# refresh
ax2.imshow(apple2, extent = loc2_coords )
# ax2.imshow(apple2_trans, extent = loc1_coords)
# recog
ax3.imshow(apple2, extent = loc1_coords )
ax3.imshow(apple2, extent = loc2_coords )
ax3.imshow(apple2, extent = loc3_coords )

x_stu=study['xstart']
y_stu=study['ystart']
nstupoints = len(y_stu)


x_ref=refresh['xstart']
y_ref=refresh['ystart']
nrefpoints = len(y_ref)

x_rec=recog['xstart']
y_rec=recog['ystart']
nrecpoints = len(y_rec)

# extra_points = nrefpoints - nstupoints
# x_stu = x_stu.append(x_stu)
# x_stu = x_stu.append(x_stu)
# y_stu = y_stu.append(y_stu)
# y_stu = y_stu.append(y_stu)
print(nstupoints, nrefpoints, nrecpoints)

maxpoints = max([nstupoints, nrefpoints, nrecpoints])

l_stu, = ax1.plot([], [], 'w-', alpha=0.5)
dot_stu, = ax1.plot([], [], 'wo', alpha=.5)

l_ref, = ax2.plot([], [], 'w-', alpha=0.5)
dot_ref, = ax2.plot([], [], 'wo', alpha=.5)

l_rec, = ax3.plot([], [], 'w-', alpha=0.5)
dot_rec, = ax3.plot([], [], 'wo', alpha=.5)

def update_line(num, x,y, line, dot):
    i = num
    if num > len(x):
        i = len(x)
    line.set_data(x[:i], y[:i])
    dot.set_data(x[i-1:i], y[i-1:i])
    return line, dot,

def update_lines(num, x_stu, y_stu, x_ref, y_ref, x_rec, y_rec, l_stu, dot_stu, l_ref, dot_ref, l_rec, dot_rec ):
    a = update_line(num, x=x_stu, y=y_stu, line=l_stu, dot=dot_stu)
    b = update_line(num, x=x_ref, y=y_ref, line=l_ref, dot=dot_ref)
    c = update_line(num, x=x_rec, y=y_rec, line=l_rec, dot=dot_rec)
    return a + b + c

line_ani = animation.FuncAnimation(fig, update_lines, maxpoints,
                                   fargs=(x_stu, y_stu, x_ref, y_ref, x_rec, y_rec, l_stu,
                                          dot_stu, l_ref, dot_ref, l_rec, dot_rec), interval=200, blit=True)
line_ani.save('../figs/eyepath_reftr'+str(ref_trial_num)+sub+'.gif', writer=writer)
