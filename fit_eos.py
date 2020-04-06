from scipy.optimize import fmin
import numpy as np


def square_differences(parameters, x_values, y_values, fit_function):
    """Return the sum of the square of difference of fit function from y-values"""
    return np.power(fit_function(parameters, x_values) - y_values, 2).sum()


def fit_eos(volumes, total_energies, fit_function, maximum_number_of_iterations=1e5):
    """Return list of parameters for requested equation of state fit to minimize sum-square difference from data"""
    # Set up initial parameters
    #   parameter[0] = E_0 -- choose minimum of total_energies to start
    initial_parameters = [np.amin(total_energies)]

    #   parameter[1] = V_0 -- choose volume corresponding to minimum energy to start
    minimum_energy_index = np.argmin(total_energies)
    initial_parameters.append(volumes[minimum_energy_index])

    #   parameter[2] = K_0 -- choose curvature around minimum energy to start
    #       K_0 = d2E / (dV)^2
    #       pick data point closest to minimum in energy
    if total_energies[minimum_energy_index+1] < total_energies[minimum_energy_index-1]:
        energy_difference = total_energies[minimum_energy_index + 1] - total_energies[minimum_energy_index]
        volume_difference = volumes[minimum_energy_index + 1] - volumes[minimum_energy_index]
    else:
        energy_difference = total_energies[minimum_energy_index - 1] - total_energies[minimum_energy_index]
        volume_difference = volumes[minimum_energy_index - 1] - volumes[minimum_energy_index]
    #       K_0 = 2 (E_1 - E_0) / (V_1 - V_0)^2
    initial_parameters.append(2 * energy_difference / np.power(volume_difference, 2))

    #   parameter[3] = d K_0 / dP -- guess 1.0 -- NEED TO DERIVE BETTER STARTING POINT
    initial_parameters.append(1.0)

    if fit_function == 'murnaghan':
        from equations_of_state import murnaghan
        parameters = fmin(square_differences, initial_parameters, args=(volumes, total_energies, murnaghan),
                          maxiter=maximum_number_of_iterations)
    elif fit_function == 'birch-murnaghan':
        from equations_of_state import birch_murnaghan
        parameters = fmin(square_differences, initial_parameters, args=(volumes, total_energies, birch_murnaghan),
                          maxiter=maximum_number_of_iterations)
    elif fit_function == 'vinet':
        from equations_of_state import vinet
        parameters = fmin(square_differences, initial_parameters, args=(volumes, total_energies, vinet),
                          maxiter=maximum_number_of_iterations)
    else:
        print("{} is not a supported equation of state".format(fit_function))
        return

    # Return parameters list output by fmin
    return parameters

