#!/bin/bash

PREFIX=Cu.Fm-3m
INPUT=$PREFIX.scf.in
PW=/usr/src/qe-6.4.1/bin/pw.x
NNODE=4
NPOOL=4

source /opt/intel/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64 

#kpoint--------------------------------------------------------------------------
for kpoint in `seq 1 1 30`
do
        input_file=$PREFIX.kpoint_$kpoint\.scf.in
        output_file=`echo $input_file | sed 's/\.in/\.out/'`
        sed '/14 14 14/s/14 14 14/'$kpoint'  '$kpoint'  '$kpoint'/' $INPUT > $input_file

        mpirun -np $NNODE $PW -npool $NPOOL -input $input_file >& $output_file
done

