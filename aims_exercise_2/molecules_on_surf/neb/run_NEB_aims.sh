#!/bin/bash
#SBATCH --account=juritala #project_2008059
#SBATCH -p medium # test - for testing 1h ; medium - up to 20 nodes/36 hours ; large - 20-200 nodes/36 hours #
#SBATCH --time=1-12:00:00      # dd-hh:mm:ss
#SBATCH -J aimsTest-array        # name 
#SBATCH -o sbatch-%j.out # where the outputs & errors are written
#SBATCH -N 4                  # N nodes to run (N x 64 = n); max 192 ; max debug 48
#SBATCH --ntasks-per-node=128                # n processes to run (N x 64 = n); max 192 ; max debug 48


# check modules.txt for updating following lines: # module purge
module load gcc/11.2.0 openmpi/4.1.2 openblas/0.3.18-omp netlib-scalapack/2.1.0 
export OMP_NUM_THREADS=1
ulimit -s unlimited
export ASE_AIMS_COMMAND="srun /scratch/juritala/FHI-aims/build_211214/aims.211214.x aims.211214.x > aims.out"
export AIMS_SPECIES_DIR="/scratch/juritala/FHI-aims/FHIaims/species_defaults/defaults_2020/light"




python NEB_n2hbc_aims_1.1.py > output.txt

echo "NEB run is finished..."


