from pathlib import *
import numpy as np
import pandas as pd

def read_behave_file(filepath):
    """read in behavearray, turn into DataFrame and delete extra columns"""
    colnames=['loc1x','loc1y','tmpx','tmpy','tmpdist','tmpmaxdist','tmpdistused','block','angle','loc3x','loc3y','loc2x','loc2y',
         'loc1-loc2dist','loc1-loc3dist','loc2-loc3dist','picid','contextid','cond',
         'study order','refresh order','recog order','same/diff','same/diff rt',
          'recog button', 'recog loc','recog rt','tmp']
    behavearray=pd.read_table(filepath,header=None,names=colnames)
    tmpmask=~behavearray.columns.str.contains('tmp')
    behavearray=behavearray[behavearray.columns[tmpmask]]
    return behavearray


def adjust_pres_coords(array,x,y,xmax=1920/2,ymax=1080/2):
    """adjustment for behavioral coords to match
    eye coords for presentation version of exp"""
    newarray=pd.DataFrame()
    newarray[x]=array[x]+xmax
    newarray[y]=(array[y]-ymax)*-1
    return newarray

def apply_adjust_pres_coords(behavearray):
    """applies adjust_pres_coords to all
    coords in behave array"""
    newloc1=adjust_pres_coords(behavearray,'loc1x','loc1y')
    newloc2=adjust_pres_coords(behavearray,'loc2x','loc2y')
    newloc3=adjust_pres_coords(behavearray,'loc3x','loc3y')
    newlocs=pd.concat([newloc1,newloc2,newloc3],axis=1)

    cols=newlocs.columns.tolist()
    for loc in cols:
        behavearray[loc]=newlocs[loc]
    return behavearray

def read_times_file_pres(timespath):
    timecolnames=['global trial start','objonset','trialend']
    timesdf=pd.read_table(timespath,header=None, names=timecolnames, index_col=False)
    print(timesdf.head())
    del timesdf['global trial start']
    return timesdf

def read_times_file_mat(timespath,phase):
    print('running',timespath)
    if phase == 'study':
        timecolnames=['tmp1', 'tmp2', 'tmp3', 'tmp4',
        'tmp5', 'tmp6', 'objonset', 'tmp7']
    else:
        timecolnames=['tmp1', 'tmp2', 'objonset','tmp3', 'tmp4']

    timesdf=pd.read_table(timespath,header=None,names=timecolnames, index_col=False)
    print(timesdf.head())
    tmp_cols=~timesdf.columns.str.contains('tmp')
    print(tmp_cols)
    timesdf=timesdf[timesdf.columns[tmp_cols]]
    timesdf['trialend']=np.nan
    return timesdf
