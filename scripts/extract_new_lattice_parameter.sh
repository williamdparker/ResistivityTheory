#!/bin/bash

OUT=$1 # first argument should be name of output file

original_a0=`grep "celldm(1)" $OUT | awk '{printf "%f",$2}'`
original_a11=`grep -A1 "crystal axes" $OUT | tail -1 | awk '{printf "%f",$4}'`
final_a11=`grep -A1 CELL $OUT | tail -1 | awk '{printf "%f",$1}'`

echo "$original_a0 $original_a11 $final_a11" | awk '{printf "%f\n",$1*$3/$2}'
