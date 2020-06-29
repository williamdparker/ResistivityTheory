#!/bin/bash

################################################################
# Things to modify/set
################################################################

#Input file prefix
PRE=Cu

#Space group name
GROUP=Fm-3m

#User-given input files
#
####Make sure nbnd is set high enough####
IN=$PRE.$GROUP.scf.in
KPTFILE=band_kpts.dat

# Parallelization parameters
NNODE=4
NPOOL=4

################################################################

source /opt/intel/bin/compilervars.sh intel64
source /opt/intel/mkl/bin/mklvars.sh intel64 

#Working directory
#WORKDIR=`pwd`

#Scratch directory
#SCRATCH=$HOME/scratch

#Location of binaries
EXE=/usr/src/qe-6.4.1/bin/pw.x
EXE2=/usr/src/qe-6.4.1/bin/bands.x

#Generated input files
IN2=$PRE.$GROUP.bands-pw.in
IN3=$PRE.$GROUP.bands.in

#Ooutput file names
OUT=`echo $IN | sed 's/\.in/\.out/'`
OUT2=`echo $IN2 | sed 's/\.in/\.out/'`
OUT3=`echo $IN3 | sed 's/\.in/\.out/'`

#Data file prefix
PREFIX=`grep prefix $IN | tr -d "', " | sed 's/^.*=//'`

DATE=`date`
echo "Time at the start of the job is: $DATE"
echo ""

make_bands_from_scf_input () {
        nkptx_scf=`grep -A1 K_POINTS $IN | tail -1 | awk '{printf "%i",$1}'`
        nkpty_scf=`grep -A1 K_POINTS $IN | tail -1 | awk '{printf "%i",$1}'`
        nkptz_scf=`grep -A1 K_POINTS $IN | tail -1 | awk '{printf "%i",$1}'`
        nkpthighsymm=`wc -l $KPTFILE | awk '{printf "%i",$1}'`
        sed '/calculation/s/scf/bands/' $IN              |\
        sed '/restart_mode/d'                            |\
        sed '/tstress/d'                                 |\
        sed '/tprnfor/d'                                 |\
        sed '/startingpot/d'                             |\
        sed '/startingwfc/d'                             |\
        sed '/K_POINTS/s/K_POINTS.*/K_POINTS crystal_b/' |\
        sed 's/.*'$nkptx_scf' '$nkpty_scf' '$nkptz_scf'.*/'$nkpthighsymm'/'
        cat $KPTFILE
}

make_bands_from_scf_input > $IN2

make_bands_input () {

        echo "&bands"
        echo "  prefix='$PREFIX',"
        echo "  outdir='./'"
        echo "  filband='$PRE.$GROUP.band'"
        echo "  lsym=.true.,"
        echo " /"
}

make_bands_input > $IN3

#Bands file
BANDS=`grep filband $IN3 | tr -d "', " | sed 's/^.*=//'`
BANDSRAP=$BANDS.rap

echo "mpirun -np $NNODE $EXE -npool $NPOOL -input $IN >& $OUT"
echo ""
mpirun -np $NNODE $EXE -npool $NPOOL -input $IN >& $OUT

echo ""
echo "Running the pw.x BANDS job:"
echo "mpirun -np $NNODE $PW -npool $NPOOL -input $IN2 >& $OUT2"
echo ""
mpirun -np $NNODE $EXE -npool $NPOOL -input $IN2 >& $OUT2

echo ""
echo "Running the bands.x BANDS job:"
echo "$EXE2 < $IN3 > $OUT3"
echo ""
mpirun -np 1 $EXE2 < $IN3 > $OUT3

DATE=`date`
echo "Final time is: $DATE"

