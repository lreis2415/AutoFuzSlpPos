#!/usr/bin/env bash
## This is an example for dgpm-cluster with CentOS 6.2.
#PBS -N pitremoveJob
#PBS -l nodes=1:ppn=4
#PBS -j oe
#PBS -m abe -M zlj@lreis.ac.cn

# Path to your executable.
cd $HOME/data

# Add any addition to your environment variables like PATH.
# For example, if your local MPI installation is in $HOME/mpich/bin
export PATH=$HOME/mpich/bin:$PATH

# Launch program using the hosts
mpiexec -n 4 $HOME/TauDEM5.3/exec/pitremove -z "pvdem.tif" -fel "pvdemfel.tif"