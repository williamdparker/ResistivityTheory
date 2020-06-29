#!/bin/bash

pref=Cu.Fm-3m
INPUT=$pref.vc-relax.in
PW=/usr/src/qe-6.4.1/bin/pw.x
NNODE=2
NPOOL=2

source /opt/intel/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64 

input_file=$INPUT 
output_file=`echo $input_file | sed 's/\.in/\.out/'`

mpirun -np $NNODE $PW -npool $NPOOL -input $input_file >& $output_file
