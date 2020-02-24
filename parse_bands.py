
import numpy as np
import re
# import matplotlib as mpl
import matplotlib.pyplot as plt

# mpl.rcParams['text.usetex'] = True
# mpl.rcParams['font.sans-serif'] = "cmr10"

THz_per_inverse_cm = 0.02998

# Get the number of bands and k-points per band, then the frequencies for each k-point

filename = 'Cu.Fm-3m.PZ.band'
with open(filename) as bandfile:
    first_line = bandfile.readline()
    number_of_bands = int(re.sub('\,', '', first_line).split()[2])
    number_of_kpoints = int(first_line.split()[4])
    bands = np.zeros((number_of_bands, number_of_kpoints))

    for line_index, line in enumerate(bandfile.readlines()):
        if line_index % 2 != 0:
            kpoint_index = int(line_index/2)
            bands[:, kpoint_index] = line.split()


print("{} bands found for {} k-points".format(number_of_bands, number_of_kpoints))


# Get x-values calculated proportionally to reciprocal space paths

#filename = 'Si.Fd-3m.freq.gp'
#kpoint_plotvalues = np.zeros(number_of_kpoints)
#with open(filename) as freqgpfile:
#    for line_index, line in enumerate(freqgpfile.readlines()):
#        kpoint_plotvalues[line_index] = line.split()[0]

# Next: read x-values of special q-points from plotband output file and decide on labels

# Make the bands plot

for band_index in range(0, number_of_bands-1):
    plt.plot(kpoint_plotvalues, bands[band_index] * THz_per_inverse_cm)

plt.show()


