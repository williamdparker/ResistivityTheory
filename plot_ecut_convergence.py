import numpy as np
import scipy.optimize as opt
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.special import lambertw

fudge_factor = 1. + 0.0e-6

# File from which to read data (should contain only [ecutwfc] [total energy])
filename = 'Cu.Fm-3m.PZ.ecutwfc_totalenergy.dat'

# Range over which to plot
total_energy_range = 1.e-1  # eV

# Data selection index
starting_data_index = 5

# 1/x^(exponent) fit
exponent = 1

# Range above and below final value to plot
convergence_threshold = 0.001  # eV

mpl.rcParams['text.usetex'] = True
# Font settings for presentation slide graphics
mpl.rcParams['font.serif'] = "Times"
mpl.rcParams['font.family'] = "serif"
mpl.rcParams['font.size'] = 18

eV_to_Rydberg = 27.211385 / 2.0

ecutwfc = []
total_energies = []
with open(filename) as ecut_file:
    for line_index, line in enumerate(ecut_file.readlines()):
        ecutwfc.append(float(line.split()[0]))
        total_energies.append(float(line.split()[1]))

# Convert total energies to eV
ecutwfc = np.array(ecutwfc)
total_energies = np.array(total_energies) * eV_to_Rydberg


def square_differences(p, x, y, f):
    return np.power(f(p, x) - y, 2).sum()


def exponential_convergence_function(parameters, input_values):
    return parameters[0] * np.exp(parameters[1] * input_values) + parameters[2]


def inverse_power_convergence_function(parameters, input_values):
    return parameters[0] * np.power(input_values, -exponent) + parameters[1]


def exponential_inverse_power_convergence_function(parameters, input_values):
    return parameters[0] * np.exp(parameters[1] * input_values) * np.power(input_values, -exponent) + parameters[2]


# Prime fit with last three values of the set
y1 = total_energies[-3]
y2 = total_energies[-2]
x1 = ecutwfc[-3]
x2 = ecutwfc[-2]
deltay12 = y1 - y2
print(deltay12)
deltax12 = x1 - x2

# Exponential fit
# c3 = total_energies[-1]
# deltay23 = abs(y2 - c3)
# print(deltay23)
# c2 = np.log(1. + deltay12 / deltay23) / deltax12
# c1 = deltay23 * np.exp(-c2 * x1)
# initial_convergence_fit_parameters = np.array([c1, c2, c3])
# print(initial_convergence_fit_parameters)
#
# exponential_convergence_fit_parameters = opt.fmin(square_differences, initial_convergence_fit_parameters,
#                                                   args=(ecutwfc[starting_data_index:],
#                                                         total_energies[starting_data_index:],
#                                                         exponential_convergence_function))
# print(exponential_convergence_fit_parameters)

# Inverse power fit
# delta_inverse_x12 = np.power(x1, -exponent) - np.power(x2, -exponent)
# inverse_power_initial_convergence_fit_parameters = np.array([(deltay12) / delta_inverse_x12, total_energies[-1]])
# print(inverse_power_initial_convergence_fit_parameters)
#
# inverse_power_convergence_fit_parameters = opt.fmin(square_differences,
#                                                     inverse_power_initial_convergence_fit_parameters,
#                                                     args=(ecutwfc[starting_data_index:],
#                                                           total_energies[starting_data_index:],
#                                                           inverse_power_convergence_function))
# print(inverse_power_convergence_fit_parameters)

# Exponential-inverse power fit
c3 = total_energies[-1]*fudge_factor   # Same as exponential fit
# product_log_argument = -x2 * np.exp(-2. + x1 / x2) / x1
# c2 = np.abs((-x1 + (2. * x2) + (x2 * lambertw(product_log_argument))) / ((x1 - x2) * x2))
# c1 = (deltay12 / deltax12) * np.exp(c2 * x2) * ((-c2 / x1) - (1. / x2))
c2 = -(deltay12 / deltax12)/y1 + (1/x1)
c1 = (y1 - c3) * x1 * np.exp(c2 * x1)
exponential_inverse_power_initial_convergence_fit_parameters = np.array([c1, c2, c3])
print(exponential_inverse_power_initial_convergence_fit_parameters)
exponential_inverse_power_convergence_fit_parameters = opt.fmin(square_differences,
                                                                exponential_inverse_power_initial_convergence_fit_parameters,
                                                                args=(ecutwfc[starting_data_index:],
                                                                      total_energies[starting_data_index:],
                                                                      exponential_inverse_power_convergence_function))

fit_ecutwfc = np.arange(10.0, ecutwfc[-1] + 20.0)
# exponential_fit_total_energies = exponential_convergence_function(exponential_convergence_fit_parameters, fit_ecutwfc)
# inverse_power_fit_total_energies = inverse_power_convergence_function(inverse_power_convergence_fit_parameters,
#                                                                      fit_ecutwfc)
exponential_inverse_power_fit_total_energies = exponential_inverse_power_convergence_function(
    exponential_inverse_power_convergence_fit_parameters, fit_ecutwfc)

# Label axes
plt.xlabel(r'$E_{\rm{cut},\psi}$ (Ry)')
plt.ylabel(r'$E_{\rm{total}}$ (eV)')

# Set vertical axis
minimum_plot_energy = total_energies[-1] - 0.01 * total_energy_range
maximum_plot_energy = total_energies[-1] + 0.09 * total_energy_range
plt.ylim([minimum_plot_energy, maximum_plot_energy])
# plt.ylim([-2830,-2820])

# Make the plot
# plt.plot(fit_ecutwfc, exponential_fit_total_energies, label=r'$e^x$')
# plt.plot(fit_ecutwfc, inverse_power_fit_total_energies, label=r'$1/x^n$')
# plt.plot(fit_ecutwfc, exponential_inverse_power_fit_total_energies, label=r'$e^x/x^n$')
c1 = exponential_inverse_power_convergence_fit_parameters[0]
c2 = exponential_inverse_power_convergence_fit_parameters[1]
c3 = exponential_inverse_power_convergence_fit_parameters[2]
exponential_inverse_power_label = r'${:.1f} \exp({:.1f}x) / x + {:.1f}$'.format(c1, c2, c3)
#plt.plot(fit_ecutwfc, exponential_inverse_power_fit_total_energies, label=exponential_inverse_power_label)
plt.plot(fit_ecutwfc, exponential_inverse_power_fit_total_energies)
plt.axhline(c3, linestyle='--', color='black')
plt.scatter(ecutwfc, total_energies)
# plt.legend()
plt.tight_layout()
plt.show()
