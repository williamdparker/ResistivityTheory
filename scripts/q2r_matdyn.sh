#!/bin/sh

PREFIX=Cu.Fm-3m

q2r_in=$PREFIX.q2r.in
q2r_out=`echo $q2r_in | sed 's/\.in/\.out/'`

matdyn_in=$PREFIX.matdyn.in
matdyn_out=`echo $matdyn_in | sed 's/\.in/\.out/'`

BIN_DIR=/usr/src/qe-6.4.1/bin
Q2R=$BIN_DIR/q2r.x
MATDYN=$BIN_DIR/matdyn.x

$Q2R  < $q2r_in > $q2r_out
$MATDYN  < $matdyn_in > $matdyn_out
