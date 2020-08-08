#! /bin/csh
#PBS -q SINGLE
#PBS -l select=1:ncpus=20:mpiprocs=20
#PBS -N p-p1
cd ${PBS_O_WORKDIR}
setenv KMP_AFFINITY disabled
setenv OMP_NUM_THREADS 1


mpiexec_mpt omplace -nt ${OMP_NUM_THREADS} ../openmx p-p1$param.dat -nt ${OMP_NUM_THREADS} > p-p1$param.std


