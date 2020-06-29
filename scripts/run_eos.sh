#!/bin/bash

PREFIX=Cu.Fm-3m
INPUT=$PREFIX.scf.in

PW=/usr/src/qe-6.4.1/bin/pw.x
NNODE=4
NPOOL=4

source /opt/intel/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64 

A0=6.797348

for strain in `seq -0.05 0.01 0.05`
do
    alatt=`echo $A0 $strain | awk '{printf "%13.11f",$1*(1+$2)}'`
    echo "Calculating total energy for celldm(1) = $alatt Bohr..."
    input_file=$PREFIX.strain_$strain\.scf.in
    output_file=`echo $input_file | sed 's/\.in/\.out/'`
    sed '/celldm/s/'$A0'/'$alatt'/' $INPUT > $input_file

    mpirun -np $NNODE $PW -npool $NPOOL -input $input_file >& $output_file
done
