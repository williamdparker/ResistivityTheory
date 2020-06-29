#!/bin/bash

PREFIX=Cu.Fm-3m
BIN_DIR=/usr/src/qe-6.4.1/bin
PW=$BIN_DIR/pw.x
PH=$BIN_DIR/ph.x
NNODE=4
NPOOL=4

source /opt/intel/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64 

mpirun -np $NNODE $PW -npool $NPOOL -input $PREFIX\.scf.in >& $PREFIX\.scf.out

mpirun -np $NNODE $PH -npool $NPOOL -input $PREFIX\.ph.in >& $PREFIX\.ph.out
