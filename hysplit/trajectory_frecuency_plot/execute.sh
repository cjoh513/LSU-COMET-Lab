 #!/usr/bin/env bash
export HYSPLIT_EXEC="/home/cometlab/Documents/Edwin/hysplit/hysplit.v5.3.4_UbuntuOS20.04.6LTS/exec"
$HYSPLIT_EXEC/trajfreq -iINFILE -ftrajfreq.bin

$HYSPLIT_EXEC/concplot -itrajfreq.bin -otrajfreq -z80 -c4 -v10+5+2+1+0.5+0.2+0.1
