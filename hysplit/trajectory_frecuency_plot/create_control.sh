#!/bin/bash

##########################
# Code to create intermediate files
##########################

# Set HYSPLIT executable paths
export PGM=/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec/
export DEV=/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec/
export EXM=/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/examples

# Directory where your BIN file is located
METDIR="/home/cometlab/Documents/Edwin/hysplit_work"
METFILE="2022-05-31_rizza.BIN"

# Output directory (must exist)
OUTDIR="./"

# Loop over each day of May 2022 (you can adjust the range)
for DAY in {22..31}; do


cat > CONTROL << EOF
1
2022 05 $DAY 00
1
18.21 -66.60 3000.0
192
0
10000.0
1
$METDIR
$METFILE
1
tdump_$DAY
EOF

# Run the trajectory model
  time ${PGM}hyts_std 001 || { echo "ERROR: HYSPLIT crashed on day $DAY"; exit 1; }

done

