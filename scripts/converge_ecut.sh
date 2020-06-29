#!/bin/bash

pref=Cu.Fm-3m
INPUT=$pref.scf.in
PW=/usr/src/qe-6.4.1/bin/pw.x
NNODE=4
NPOOL=4

source /opt/intel/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64 

#ecut---------------------------------------------------------------------------
ecut0=$(awk '/ecut/ {print $3}' $INPUT)

for ecut in `seq 510 10 600`
do
	input_file=$pref.ecut_$ecut\.scf.in
	output_file=`echo $input_file | sed 's/\.in/\.out/'`
	sed "/ecut/s/$ecut0/$ecut/" $INPUT > $input_file
	
	mpirun -np $NNODE $PW -npool $NPOOL -input $input_file >& $output_file
done

#mkdir -p betasn/ecut/
#mv -f $pref.ecut* betasn/ecut
