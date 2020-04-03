import matplotlib as mpl
import matplotlib.pyplot as plt

# Use TeX fonts
mpl.rcParams['text.usetex'] = True

# Font settings for presentation slide graphics
mpl.rcParams['font.serif'] = "Times"
mpl.rcParams['font.family'] = "serif"
mpl.rcParams['font.size'] = 18

# Import volumes from simulation data as numpy array simulation_volumes
# Fit an equation of state (Vinet or Birch-Murnaghan) to the data
# Create an array of volumes with fine spacing as numpy array fit_volumes
# Evaluate the fit function on the fit_volumes array and save to fit_total_energies

plt.plot(fit_volumes, fit_total_energies)
plt.scatter(simulation_volumes, simulation_total_energies)
plt.title(r'Energy Equation of State for ' + structure_names[0] + ' ' + chemical_formula)
plt.xlabel(r'Volume (m$^3$/atom)')
plt.ylabel(r'Total Energy (eV/atom)')

plt.show()
