 #!/usr/bin/env bash
export HYSPLIT_EXEC="/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec"

# Put all the tdump files in the file called INFILE
ls tdump_* > INFILE

# Get the trajectories
$HYSPLIT_EXEC/trajfreq -iINFILE -ftrajfreq.bin

# Plot the frecuency plot
$HYSPLIT_EXEC/concplot -itrajfreq.bin -otrajfreq -z80 -c4 -v10+5+2+1+0.5+0.2+0.1
