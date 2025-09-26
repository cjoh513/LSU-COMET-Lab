#!/usr/bin/env bash

HYSPLIT_EXEC="/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec/"



echo "'TITLE&','Trajectory Matrix (006)&'" >LABELS.CFG
cp CONTROL.006 CONTROL
${HYSPLIT_EXEC}latlon
time ${HYSPLIT_EXEC}hyts_std || die "ERROR: HYSPLIT crashed"
${HYSPLIT_EXEC}trajplot -s1 -l0 -z90 -itdump_006 -oplot_006.ps
rm -f CONTROL MESSAGE LABELS.CFG TRAJ.CFG MESSAGE.006
cat plot_006.ps >>results.ps

