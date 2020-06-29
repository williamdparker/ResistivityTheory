#!/bin/bash

OUT=$1 # first argument should be name of output file

natom=`grep "number of atoms" $OUT | awk '{printf "%i",$5}'`

final_coordinates=`grep -A$natom ATOMIC_POSITIONS $OUT | tail -$natom`

echo "$final_coordinates"
