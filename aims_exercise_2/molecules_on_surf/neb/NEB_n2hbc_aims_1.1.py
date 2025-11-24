import os
from ase.io import read
from ase import units
from ase.constraints import FixAtoms
from ase.calculators.aims import Aims, AimsProfile
from ase.mep import NEB
from ase.optimize.fire import FIRE as QuasiNewton

# Read initial and final geometries
initial = read('nacl_traj_0.in')
final = read('nacl_traj_0.in')

# Define calculators for initial/final states
initial_calc = Aims(
    profile=AimsProfile(command=os.environ['ASE_AIMS_COMMAND']),
    xc="pbe",
    charge=0,
    spin="none",
    k_grid=[1, 1, 1],
    relativistic=["atomic_zora", "scalar"],
    compute_forces=True,
    occupation_type=["gaussian", 0.01],
    vdw_ts='vdw_params_kind=tssurf',
    charge_mix_param=0.10,
    sc_iter_limit=400,
    compensate_multipole_errors=True,
    load_balancing=True
)

# Attach calculator and compute forces for initial state
initial.calc = initial_calc
initial_energy = initial.get_potential_energy()
initial_forces = initial.get_forces()

final_calc = Aims(
    profile=AimsProfile(command=os.environ['ASE_AIMS_COMMAND']),
    xc="pbe",
    charge=0,
    spin="none",
    k_grid=[1, 1, 1],
    relativistic=["atomic_zora", "scalar"],
    compute_forces=True,
    occupation_type=["gaussian", 0.01],
    vdw_ts='vdw_params_kind=tssurf',
    charge_mix_param=0.10,
    sc_iter_limit=400,
    compensate_multipole_errors=True,
    load_balancing=True
)

# Attach calculator and compute forces for final state
final.calc = final_calc
final_energy = final.get_potential_energy()
final_forces = final.get_forces()

# Create intermediate images (including initial and final)
images = [initial]

for i in range(8):
    images.append(initial.copy())

# Define calculator for all images
for image in images[1:]:
    image.calc = Aims(
    profile=AimsProfile(command=os.environ['ASE_AIMS_COMMAND']),
    xc="pbe",
    charge=0,
    spin="none",
    k_grid=[1, 1, 1],
    relativistic=["atomic_zora", "scalar"],
    compute_forces=True,
    occupation_type=["gaussian", 0.01],
    vdw_ts='vdw_params_kind=tssurf',
    charge_mix_param=0.10,
    sc_iter_limit=400,
    compensate_multipole_errors=True,
    load_balancing=True)

# Append final image
images.append(final)

# Constrain substrate atoms
constraint = FixAtoms(mask=[atom.symbol in {'Na', 'Cl', 'Au'} for atom in initial])
for image in images:
    image.set_constraint(constraint)

# Run IDPP interpolation
neb = NEB(images)
neb.interpolate('idpp')

# Run NEB optimization
qn = QuasiNewton(neb, trajectory='c_c_cleavage.traj', logfile='c_c_cleavage.log')
qn.run(fmax=0.05)

