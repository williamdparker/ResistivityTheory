#!/bin/bash

HOSTS=pleiades10 
SCF_INPUT=Cu.Fm-3m.scf.in
SCF_OUTPUT=`echo $SCF_INPUT | sed 's/\.in/\.out/'`
NSCF_INPUT=`echo $SCF_INPUT | sed 's/scf\.in/nscf\.in/'`
NSCF_OUTPUT=`echo $NSCF_INPUT | sed 's/\.in/\.out/'`
PW=/usr/src/qe-6.4.1/bin/pw.x
NNODE=4
NPOOL=4

source /opt/intel/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64 

mpirun -np $NNODE -hosts $HOSTS $PW -npool $NPOOL -input $SCF_INPUT >& $SCF_OUTPUT
mpirun -np $NNODE -hosts $HOSTS $PW -npool $NPOOL -input $NSCF_INPUT >& $NSCF_OUTPUT
