import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from fit_eos import fit_eos
from unit_conversions import cubic_bohr_to_cubic_meter, cubic_meter_to_cubic_angstrom
from unit_conversions import joule_to_electron_volt, rydberg_to_joule

# Use TeX fonts
mpl.rcParams['text.usetex'] = True

# Font settings for presentation slide graphics
mpl.rcParams['font.serif'] = "Times"
mpl.rcParams['font.family'] = "serif"
mpl.rcParams['font.size'] = 18

# Simulation system description
structure_name = 'Fm-3m'
number_of_atoms = 1
chemical_formula = 'Cu'
exchange_correlation = 'PZ'
filename = chemical_formula + '.' + structure_name + '.' + exchange_correlation + '.volume_total_energy.dat'
atomic_filename = chemical_formula + '.atom.' + exchange_correlation + '.dat'

# Parameters
number_of_fit_volumes = 50
output_units = 'electron_volt_angstrom'  # eV-Å or J-m

# Import data from file     (assuming units of bohr^3, Ry)
simulation_volumes = []
simulation_total_energies = []
with open(filename) as eos_file:
    for line_index, line in enumerate(eos_file.readlines()):
        simulation_volumes.append(float(line.split()[0]))
        simulation_total_energies.append(float(line.split()[1]))

with open(atomic_filename) as atomic_file:
    for line_index, line in enumerate(atomic_file.readlines()):
        atomic_energy = float(line.split()[0])

# Convert lists to NumPy arrays
simulation_volumes = np.asarray(simulation_volumes)
simulation_total_energies = np.asarray(simulation_total_energies)

# Convert units
simulation_volumes = simulation_volumes * cubic_bohr_to_cubic_meter
simulation_total_energies = simulation_total_energies * rydberg_to_joule
atomic_energy *= rydberg_to_joule

# Convert to units per atom
simulation_volumes, simulation_total_energies = simulation_volumes/number_of_atoms, \
                                                simulation_total_energies/number_of_atoms

print("Simulation volumes (m^3/atom):")
print(simulation_volumes)
print("Simulation total energies (J/atom):")
print(simulation_total_energies)
print("Atomic total energy (J/atom):")
print(atomic_energy)

# from Cohen et al. (2000) Accuracy of equation-of-state formulations
#
# "For strains less than 30%, it probably doesn’t matter what equation of state you use, as was emphasized by
# Jeanloz (1988), but parameters will still be better determined with the Vinet equation (see also Hemley et al. 1990).
# For large strains, the Vinet equation is best, and forms such as the Holzapfel equation are required at extreme
# compressions."
fit_function = 'vinet'

# Set up volume array to start and stop with simulated volumes
minimum_volume = np.amin(simulation_volumes)
maximum_volume = np.amax(simulation_volumes)
fit_volumes = np.linspace(minimum_volume, maximum_volume, num=number_of_fit_volumes)

if fit_function == 'murnaghan':
    from equations_of_state import murnaghan
    parameters = fit_eos(simulation_volumes, simulation_total_energies, murnaghan)
    fit_total_energies = murnaghan(parameters, fit_volumes)
elif fit_function == 'birch-murnaghan':
    from equations_of_state import birch_murnaghan
    parameters = fit_eos(simulation_volumes, simulation_total_energies, birch_murnaghan)
    fit_total_energies = birch_murnaghan(parameters, fit_volumes)
elif fit_function == 'vinet':
    from equations_of_state import vinet
    parameters = fit_eos(simulation_volumes, simulation_total_energies, vinet)
    print("Vinet equation of state parameters found:")
    print("\tEquilibrium energy      (J/atom)   = {:.3e}".format(parameters[0]))
    print("\tBulk modulus            (Pa)       = {:.3e}".format(parameters[1]))
    print("\tBulk modulus derivative            = {:.3e}".format(parameters[2]))
    print("\tEquilibrium volume      (m^3/atom) = {:.3e}".format(parameters[3]))
    fit_total_energies = vinet(parameters, fit_volumes)
    cohesive_energy = -1*(parameters[0] - atomic_energy) * joule_to_electron_volt
    print("\tCohesive energy         (eV/atom)  = {:.3f}".format(cohesive_energy))

# Make plot
# plt.title(r'Energy Equation of State for ' + structure_name + ' ' + chemical_formula)
if output_units == 'joule_meter':
    plt.xlabel(r'Volume (m$^3$/atom)')
    plt.ylabel(r'Total Energy (J/atom)')
elif output_units == 'electron_volt_angstrom':
    fit_volumes = fit_volumes * cubic_meter_to_cubic_angstrom
    simulation_volumes = simulation_volumes * cubic_meter_to_cubic_angstrom
    fit_total_energies = fit_total_energies * joule_to_electron_volt
    simulation_total_energies = simulation_total_energies * joule_to_electron_volt
    plt.xlabel(r'Volume (Å$^3$/atom)')
    plt.ylabel(r'Total Energy (eV/atom)')
else:
    print("{} units not implemented".format(output_units))
    exit()

# Formatting future points
#   x-range = 210% of max(V_0 - V_max, V_0 - V_min) centered at V_0
#   y-range = 160% of max(E(V_max)-E(V_0), E(V_min)-E(V_0)) centered in middle
#   Data summary to right of plot   E_coh,0 = ... eV/atom
#                                   V_0     = ... Å^3/atom
#                                   K_0     = ... GPa
#                                   K_0'    = ...




plt.plot(fit_volumes, fit_total_energies)
plt.scatter(simulation_volumes, simulation_total_energies)
plt.show()
