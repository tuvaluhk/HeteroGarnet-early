#!/usr/bin/env bash
#
# Script for running DSENT for a given simulation output directory

if [ "$#" -lt 1 ]; then
    echo "Please specify a simulation output directory"
    exit
fi

for outdir in "$@"; do
    if [ ! -f $outdir/stats.txt ]; then
        echo "$outdir/stats.txt not found"
        continue
    fi
    DSENT_OUT=$outdir/dsent_out.txt
    echo "Writing DSENT power and area model to: $DSENT_OUT"
    python2.7 /home/tuvalu/Documents/HeteroGarnet-early/util/on-chip-network-power-area-2.0.py $outdir &> $DSENT_OUT
done
