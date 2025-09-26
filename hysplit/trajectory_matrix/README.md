# HYSPLIT Trajectory Matrix Execution Guide

This guide explains how to execute a HYSPLIT trajectory matrix simulation.

---

## 1. Copy Necessary Files

Make sure to copy the same files from the trajectory ensemble before running the execution.

---

## 2. Set the Variables

Edit the file **`CONTROL.006`**:

```bash
vim CONTROL.006
Example content of CONTROL.006:

yaml
Copy code
00 00 00 00
3
14.5  21.0 1500.0  # lat, lon, corner in the bottom-right
24.0 -14.0 1500.0  # lat, lon, corner in the upper-left
18.5  25.0 1500.0  # spacing between simulations (lat diff = 4° here)
9999               # number of simulations (e.g., 24 hours for one day or 99999 to use all data)
0
10000.0
1
/home/cometlab/Downloads/delete/
aer_ra_feedback_1_20220531_20220616
./
tdump_006
```

## 3. Create the Execution File
Edit the script run_trajectory.sh:

```bash
Copy code
vim run_trajectory.sh
```
Content of the script:

```bash

#!/usr/bin/env bash

HYSPLIT_EXEC="/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec/"

echo "'TITLE&','Trajectory Matrix (006)&'" > LABELS.CFG
cp CONTROL.006 CONTROL
${HYSPLIT_EXEC}latlon
time ${HYSPLIT_EXEC}hyts_std || die "ERROR: HYSPLIT crashed"
${HYSPLIT_EXEC}trajplot -s1 -l0 -z90 -itdump_006 -oplot_006.ps
rm -f CONTROL MESSAGE LABELS.CFG TRAJ.CFG MESSAGE.006
cat plot_006.ps >> results.ps
```

✅ Now you can run the script:

```bash

bash run_trajectory.sh
```
<img width="875" height="889" alt="image" src="https://github.com/user-attachments/assets/ac72aa0d-33f1-46fb-beb1-fa08e7cdd46b" />

