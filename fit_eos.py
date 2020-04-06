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

    #   parameter[1] = K_0 -- choose curvature around minimum energy to start
    #       K_0 = V_0 * d2E / (dV)^2
    #       pick data point closest to minimum in energy
    minimum_energy_index = np.argmin(total_energies)
    second_derivative_numerator = total_energies[minimum_energy_index+1] - \
                                  2*total_energies[minimum_energy_index] + \
                                  total_energies[minimum_energy_index-1]
    left_volume_difference = volumes[minimum_energy_index - 1] - volumes[minimum_energy_index]
    right_volume_difference = volumes[minimum_energy_index] - volumes[minimum_energy_index + 1]
    second_derivative_denominator = left_volume_difference * right_volume_difference
    second_derivative = second_derivative_numerator / second_derivative_denominator
    initial_parameters.append(volumes[minimum_energy_index] * second_derivative)

    #   parameter[2] = d K_0 / dP -- guess 1.0 -- NEED TO DERIVE BETTER STARTING POINT
    initial_parameters.append(1.1)

    #   parameter[3] V_0 -- choose volume corresponding to minimum energy to start
    initial_parameters.append(volumes[minimum_energy_index])

    print("Initial parameters for fit:")
    print("\tEquilibrium energy      (J/atom)   = {}".format(initial_parameters[0]))
    print("\tBulk modulus            (Pa)       = {}".format(initial_parameters[1]))
    print("\tBulk modulus derivative            = {}".format(initial_parameters[2]))
    print("\tEquilibrium volume      (m^3/atom) = {}".format(initial_parameters[3]))

    if fit_function == 'murnaghan' or fit_function.__name__ == 'murnahgan':
        from equations_of_state import murnaghan
        parameters = fmin(square_differences, initial_parameters, args=(volumes, total_energies, murnaghan),
                          maxiter=maximum_number_of_iterations)
    elif fit_function == 'birch-murnaghan' or fit_function.__name__ == 'birch-murnaghan':
        from equations_of_state import birch_murnaghan
        parameters = fmin(square_differences, initial_parameters, args=(volumes, total_energies, birch_murnaghan),
                          maxiter=maximum_number_of_iterations)
    elif fit_function == 'vinet' or fit_function.__name__ == 'vinet':
        from equations_of_state import vinet
        parameters = fmin(square_differences, initial_parameters, args=(volumes, total_energies, vinet),
                          maxiter=maximum_number_of_iterations)
    else:
        print("{} is not a supported equation of state".format(fit_function))
        return

    # Return parameters list output by fmin
    return parameters

