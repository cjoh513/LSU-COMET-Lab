#!/usr/bin/env bash

# -------------------------------------------------------------
# Batch‑run HYSPLIT trajectories every 6 h between two UTC stamps
# and save each output as tdump_YYYYMMDDHH
# -------------------------------------------------------------

HYSPLIT_EXEC="/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec"
CONTROL_TEMPLATE="CONTROL_TEMPLATE.001"   # template with @YY@ @MM@ @DD@ @HH@ @YYYYMMDDHH@
START="2022-05-31 00:00"                  # first start time  (UTC)
END="2022-06-02 21:00"                    # last  start time  (UTC)
STEP_HR=6                                   # hours between successive starts

# ---------- no editing needed below this line ----------------

start_epoch=$(date -u -d "$START" +%s) || { echo "Bad START time"; exit 1; }
end_epoch=$(  date -u -d "$END"   +%s) || { echo "Bad END time";   exit 1; }
step_sec=$(( STEP_HR * 3600 ))

curr_epoch=$start_epoch
while [ $curr_epoch -le $end_epoch ]; do
    # ── format date/time strings ──────────────────────────────
    YY=$(date -u -d "@$curr_epoch" +%y)
    MM=$(date -u -d "@$curr_epoch" +%m)
    DD=$(date -u -d "@$curr_epoch" +%d)
    HH=$(date -u -d "@$curr_epoch" +%H)
    YYYYMMDDHH=$(date -u -d "@$curr_epoch" +%Y%m%d%H)
    disp=$(date -u -d "@$curr_epoch" +"%Y-%m-%d %H:%M")

    echo "\n▶ Running trajectory for $disp UTC"   

    # ── build CONTROL.001 from template ──────────────────────
    sed -e "s/@YY@/$YY/" \
        -e "s/@MM@/$MM/" \
        -e "s/@DD@/$DD/" \
        -e "s/@HH@/$HH/" \
        -e "s/@YYYYMMDDHH@/$YYYYMMDDHH/" \
        "$CONTROL_TEMPLATE" > CONTROL.001

    # ── run HYSPLIT ──────────────────────────────────────────
    "$HYSPLIT_EXEC/hyts_std" 001 || { echo "  ⚠️  HYSPLIT stopped with error ($?)"; }

    # ── keep the tdump if it was produced ────────────────────
    if [ -f tdump ]; then
        mv tdump "tdump_${YYYYMMDDHH}"
    fi

    # ── advance to next start time ───────────────────────────
    curr_epoch=$(( curr_epoch + step_sec ))
done

echo "\n✅ All done — check tdump_YYYYMMDDHH files."

