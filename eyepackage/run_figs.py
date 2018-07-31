import numpy as np
import pandas as pd
from eyepackage.organize_eyebehave_for_figs import *
from eyepackage.make_eyebehave_figs import *


sublist=['ec105', 'ec106', 'ec107', 'ec108']
phaselist=['study','refresh','recog']
roi_list=['loc1start', 'loc2start', 'loc3start', 'screen']

roi_prop_tidy_dict = {}
for phase in phaselist:
    all_eye_events=read_eye_data(sublist, phase)
    fix=get_fixations(all_eye)
    roi_prop_tidy=get_tidy_prop_viewing(fix, roi_list)
    roi_prop_tidy_dict[phase] = roi_prop_tidy

all_behave=read_behave_data(sublist)
recog_prop_tidy=get_tidy_prop_recog(all_behave)
