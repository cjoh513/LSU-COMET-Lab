#!/bin/bash

# Activate the variables
source /work/etorresm/wrf/Build_WRF/var_env.sh

EXEC_PATH="/work/etorresm/hysplit_data2arl/arw2arl"
FILES=(
"wrfout_d01_2022-05-31_00:00:00"
"wrfout_d01_2022-06-03_18:00:00"
"wrfout_d01_2022-06-07_12:00:00"
"wrfout_d01_2022-06-11_06:00:00"
"wrfout_d01_2022-06-15_00:00:00"
)

for file in "${FILES[@]}"; do
    echo "Processing $file..."
    $EXEC_PATH/./arw2arl "$file"

    # Extract the date portion and format it to YYYY-MM-DD
    date_part=$(echo "$file" | cut -d'_' -f3)

    # Rename the output
    mv ARLDATA.BIN "${date_part}.BIN"
done
