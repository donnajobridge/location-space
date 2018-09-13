*Project information:*
Experiment from Eyes are the Window to the Brain (http://www.donnajobridge.com/eyes.html)

*Step 1:*
Create individual subject arrays linking eye movements & behavioral data, and arrays with just behavioral data for plotting overview of eye movements and behavior.
*How to run:*
Go to the eyepackage directory. From there, run `python runEyeBehaveAnalysis.py`

*Step 2:*
Create the following figures of eye movement data and behavioral performance.

Eye movements:
The following graphs are created for each phase of the experiment: Study, Refresh, Recognition

All figures are bar plots showing viewing behavior for the following locations: Original, Updated, New, and Background Screen. Bar plots are made separately for Match & Mismatch conditions.

- average proportion of viewing each location
- average fixation duration at each locations
- average number of fixations to each location

Behavior:
One graph is created to show final recognition performance. A violin plot shows proportion of location selection responses on the final test for the Match & Mismatch conditions.

*How to run:*
From the eyepackage directory, run `python run_figs.py`

*Step 3:*
Created line plot showing the proportion of viewing each object-location over the course of the 5-second trial. This plot is only created for the Refresh & Recognition phases. Line plots are created for Match & Mismatch conditions separately.

For each phase, two line plots are Created
- proportion of viewing each location across all trials
- proportion of viewing each location for only those trials in which subjects selected the Original location on the final test (memory stability)

*How to run:*
From eyepackage directory, run `python run_timeseries.py`

*Step 4:*
Create gif of eye movements for one object across all three phases of the experiment: Study, Refresh, and Recognition. An apple is always plotted as the object (for display purposes only). Eye movements are shown for one subject (ec108). Any trial can be selected. Current selection is for Refresh trial 30 and Refresh trial 74 (both Mismatch trials).

*How to run:*
From eyepackage directory, run `python make_eyepath_gif_3phases.py`

*Step 5:*
Create gif of iEEG data time-locked to fixation directed to Original object-location during Refresh. iEEG data has been filtered at 5 Hz to highlight the theta frequency (3-8 Hz). Two trials from one hippocampal electrode are included, Refresh trial 30 and Refresh trial 74 for subject ec108.

*How to run:*
From eyepackage directory, run `python make_brain_animation.py`
