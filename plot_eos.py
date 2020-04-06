import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from fit_eos import fit_eos

# Use TeX fonts
mpl.rcParams['text.usetex'] = True

# Font settings for presentation slide graphics
mpl.rcParams['font.serif'] = "Times"
mpl.rcParams['font.family'] = "serif"
mpl.rcParams['font.size'] = 18

# Simulation system description
structure_name = 'Fm-3m'
chemical_formula = 'Cu'
exchange_correlation = 'PZ'
filename = chemical_formula + '.' + structure_name + '.' + exchange_correlation + '.volume_total_energy.dat'

# Parameters
number_of_fit_volumes = 50

# Import data from file     (assuming units of Å^3/atom, eV/atom)
simulation_volumes = []
simulation_total_energies = []
with open(filename) as eos_file:
    for line_index, line in enumerate(eos_file.readlines()):
        simulation_volumes.append(float(line.split()[0]))
        simulation_total_energies.append(float(line.split()[1]))

simulation_volumes = simulation_volumes * 1e-30  # convert Å^3 to m^3

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
    fit_total_energies = vinet(parameters, fit_volumes)

# Make plot
plt.plot(fit_volumes, fit_total_energies)
plt.scatter(simulation_volumes, simulation_total_energies)
plt.title(r'Energy Equation of State for ' + structure_name + ' ' + chemical_formula)
plt.xlabel(r'Volume (m$^3$/atom)')
plt.ylabel(r'Total Energy (eV/atom)')

plt.show()
