import numpy as np


def murnaghan(parameters, volumes):
    """
    Murnaghan equation of state: E(V) = E_0 + K_0 V_0 [ (1 / (K_0' (K_0' - 1))) (V / V_0)^(-(K_0' - 1)) +
                                                        (1 / K_0') (V / V_0) -

                                                        (1 / (K_0' - 1)) ]

    :param parameters: list of equation of state parameters  -  equilibrium energy (E_0),
                                                                bulk modulus (K_0),
                                                                bulk modulus pressure derivative (K_0'),
                                                                equilibrium volume (V_0)
    :param volumes: NumPy array of volumes per atom
    :return: NumPy array of Murnaghan equation of state values at input volumes
    """
    k0pm1 = p[2] - 1.0  # K_0' - 1
    return parameters[0] + (parameters[1] * parameters[3] *
                            (((1.0 / (parameters[2] * k0pm1)) * np.power((volumes / parameters[3]), (-k0pm1))) +
                             (volumes / (parameters[2] * parameters[3])) - (1.0 / k0pm1)))


def birch_murnaghan(parameters, volumes):
    """
    Birch-Murnaghan equation of state: E(V) = E_0 + (9/16) K_0 V_0 {[ (V / V_0)^(-(2/3)) - 1 ]^3 K_0' +
                                                                    [ (V / V_0)^(-(2/3)) - 1]^2 *
                                                                    [ 6 - 4 (V / V_0)^(-(2/3)) ]}
    :param parameters: list of equation of state parameters     equilibrium energy (E_0),
                                                                bulk modulus (K_0),
                                                                bulk modulus pressure derivative (K_0'),
                                                                equilibrium volume (V_0)
    :param volumes: NumPy array of volumes per atom
    :return: NumPy array of the Birch-Murnaghan equation of state values at input volumes
    """
    reduced_volume_area = np.power(volumes / parameters[3], -2 / 3)
    return parameters[0] + (9. * parameters[1] * parameters[3] / 16.) * (
            np.power(reduced_volume_area - 1., 3.) * parameters[2] +
            np.power(reduced_volume_area - 1., 2.) * (6. - 4. * reduced_volume_area))


def vinet(parameters, volumes):
    """
    Vinet equation of state: E(V) = E_0 + (4 K_0 V_0 / (K_0' - 1)^2)
                                        - (2 K_0 V_0 / (K_0' - 1)^2) (5 + 3 K_0' ((V / V_0)^(1/3) - 1)
                                                                        - 3 (V / V_0)^(1/3))
                                                                    exp(- (3/2) (K_0' - 1) (1 - (V / V_0)^(1/3)))
    :param parameters: list of equation of state parameters     equilibrium energy (E_0),
                                                                bulk modulus (K_0),
                                                                bulk modulus pressure derivative (K_0'),
                                                                equilibrium volume (V_0)
    :param volumes: NumPy array of volumes per atom
    :return: NumPy array of the Vinet equation of state values at input volumes
    """
    k0pm1 = parameters[2] - 1  # K_0' - 1
    k0pm1_squared = np.power(k0pm1, 2)
    reduced_volume_lengths = np.power(volumes / parameters[3], 1 / 3)
    return parameters[0] + (4. * parameters[1] * parameters[3] / k0pm1_squared) \
                         + (2. * parameters[1] * parameters[3] / k0pm1_squared) * \
                           (5. + 3. * parameters[2] * (reduced_volume_lengths - 1.) - 3. * reduced_volume_lengths) * \
                           np.exp(-1.5 * k0pm1 * (reduced_volume_lengths - 1))


