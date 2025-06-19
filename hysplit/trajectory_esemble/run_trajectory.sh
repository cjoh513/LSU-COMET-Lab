#!/usr/bin/env bash

HYSPLIT_EXEC="/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec/"



# -------------------------
echo "'TITLE&','Forward Trajectory (001)&'" >LABELS.CFG
time ${HYSPLIT_EXEC}hyts_std 001 || die "ERROR: HYSPLIT crashed"
${HYSPLIT_EXEC}trajplot -itdump_001 -oplot_001.ps
rm -f LABELS.CFG TRAJ.CFG MESSAGE.001
cat plot_001.ps >results.ps

# ------------------------
echo "'TITLE&','Trajectory Ensemble (005)&'" >LABELS.CFG
time ${HYSPLIT_EXEC}hyts_ens 001 || die "ERROR: HYSPLIT crashed"
${HYSPLIT_EXEC}trajplot -itdump_001 -oplot_001.ps
rm -f LABELS.CFG TRAJ.CFG MESSAGE.005

