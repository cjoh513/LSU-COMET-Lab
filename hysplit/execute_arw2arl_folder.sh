#!/bin/bash

# Activate the variables
source /work/etorresm/wrf/Build_WRF/var_env.sh

TARGET_DIR="/work/etorresm/wrf/2022-05-31_2022-06-16_rizza/feedback_1"
JOINED_FILE="2022-05-31_2022-06-16_rizza_feedback_1.BIN"
 
OUTPUT_DIR="/work/etorresm/wrf/hysplit_pre"
EXEC_PATH="/work/etorresm/hysplit_data2arl/arw2arl"
# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"
 
# Change to the target directory
cd "$TARGET_DIR" || { echo "Failed to enter target directory"; exit 1; }
 
# Collect and sort wrfout_d01 files
FILES=( $(ls -1 wrfout_d01_*  | grep -E ':00$' | sort) )

JOIN_LIST=()

for file in "${FILES[@]}"; do
    echo "Processing $file..."
    "$EXEC_PATH"/./arw2arl "$file"
 
    # Extract the date portion and format it to YYYY-MM-DD
    date_part=$(echo "$file" | cut -d'_' -f3)

    output_bin="$OUTPUT_DIR/${date_part}.BIN"
    mv ARLDATA.BIN "$output_bin"
    JOIN_LIST+=("$output_bin")
done

# Join the files in the specified order into one final BIN file
cd "$OUTPUT_DIR" || { echo "Failed to enter output directory"; exit 1; }
echo "Joining files into $JOINED_FILE..."
for file in "${JOIN_LIST[@]}"; do
    echo "Adding $file to $JOINED_FILE"
    cat "$file" >> "$JOINED_FILE"
done
echo "All files processed and joined into $JOINED_FILE"

## Delete intermediate BIN files
#for file in "${JOIN_LIST[@]}"; do
#    echo "Removing $file"              
#    rm -f "$file"                      
#done
#
#echo "Intermediate BIN files deleted."


