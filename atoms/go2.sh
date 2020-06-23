#! /bin/csh
#PBS -q SMALL
#PBS -l select=8:ncpus=20:mpiprocs=20
#PBS -N p-p239
cd ${PBS_O_WORKDIR}
setenv KMP_AFFINITY disabled
setenv OMP_NUM_THREADS 1

mpiexec_mpt omplace -nt ${OMP_NUM_THREADS} ../openmx p-p2390.dat -nt ${OMP_NUM_THREADS} > p-p2390.std
