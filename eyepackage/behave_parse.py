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

def change_behave_coords(subids):
    """create dict that assigns boolean values to indicate if
    behavioral coords should be changed to match eye coords"""
    subdict_change_coords={}
    for index,s in enumerate(subids):
        subdict_change_coords[s]=False
        if index<2:
            continue
        subdict_change_coords[s]=True
            
    return subdict_change_coords


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

def read_times_file(timespath):
    timecolnames=['global trial start','objonset','trialend']
    timesdf=pd.read_table(timespath,header=None,names=timecolnames)
    del timesdf['global trial start']
    del timesdf['trialend']
    return timesdf
