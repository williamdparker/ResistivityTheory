
import numpy as np
import re
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams['text.usetex'] = True
# Font settings for presentation slide graphics
mpl.rcParams['font.serif'] = "Times"
mpl.rcParams['font.family'] = "serif"
mpl.rcParams['font.size'] = 18


# Get the number of bands and k-points per band, then the frequencies for each k-point

filename = 'Cu.Fm-3m.PZ.band'
with open(filename) as bands_file:
    first_line = bands_file.readline()
    number_of_bands = int(re.sub('\,', '', first_line).split()[2])
    number_of_kpoints = int(first_line.split()[4])
    bands = np.zeros((number_of_bands, number_of_kpoints))
    kpoints = np.zeros((3, number_of_kpoints))

    kpoint_index = 0
    for line_index, line in enumerate(bands_file.readlines()):
        if kpoint_index == number_of_kpoints:
            break
        if line_index % 3 == 0:
            kpoints[:, kpoint_index] = line.split()
        if line_index % 3 == 1:
            bands[0:10, kpoint_index] = line.split()
        if line_index % 3 == 2:
            bands[10, kpoint_index] = line.split()[0]
            kpoint_index += 1

print("{} bands found for {} k-points".format(number_of_bands, number_of_kpoints))

# Shift bands by subtracting Fermi energy
fermi_energy = 14.4904 # eV               WARNING: TAKEN FROM PW.X SCF OUTPUT
bands = bands - fermi_energy

# Get x-values calculated proportionally to reciprocal space paths
filename = 'Cu.Fm-3m.PZ.bands.out'
with open(filename) as bands_output_file:
    kpoint_mappings = []
    for line in bands_output_file:
        if line.startswith("     high-symmetry point:"):
            kpoint_mappings.append(float(line[63:71]))

print(kpoint_mappings)
number_of_high_symmetry_points = len(kpoint_mappings)

# Ignorant way to plot (evenly spaced everywhere)
# kpoint_plotvalues = np.linspace(0.0, kpoint_mappings[-1], number_of_kpoints)

# Determine high-symmetry k-points and match with kpoints array
high_symmetry_kpoints = np.zeros((3, number_of_high_symmetry_points))
with open(filename) as bands_output_file:
    high_symmetry_kpoint_index = 0
    for line in bands_output_file:
        if line.startswith("     high-symmetry point:"):
            current_kpoint = [float(line[27:33]), float(line[35:41]), float(line[43:49])]
            high_symmetry_kpoints[:, high_symmetry_kpoint_index] = current_kpoint
            high_symmetry_kpoint_index += 1

# Next: read x-values of special q-points from plotband output file
number_of_inbetween_points = 10    # WARNING: THIS IS HARD-CODED FROM PW.X BANDS INPUT FILE
jump_point_indices = [9, 11]       # WARNING: THIS IS HARD-CODED FROM PW.X BANDS INPUT FILE
index = 0
kpoint_plotvalues = np.linspace(kpoint_mappings[index], kpoint_mappings[index + 1],
                                num=number_of_inbetween_points, endpoint=False)
index += 1
while index < number_of_high_symmetry_points-1:
    if index in jump_point_indices:
        kpoint_plotvalues = np.append(kpoint_plotvalues, float(kpoint_mappings[index]))
    else:
        next_kpoint_plotvalues = np.linspace(kpoint_mappings[index], kpoint_mappings[index+1],
                                             num=number_of_inbetween_points, endpoint=False)
        kpoint_plotvalues = np.append(kpoint_plotvalues, next_kpoint_plotvalues)
    index += 1

kpoint_plotvalues = np.append(kpoint_plotvalues, float(kpoint_mappings[-1]))

# Label high-symmetry points
# high_symmetry_kpoint_labels = ['Γ', 'X', 'W', 'K', 'Γ', 'L', 'U', 'W', 'L', 'K | U', '', 'Γ']  # Unicode
high_symmetry_kpoint_labels = [r'$\Gamma$', 'X', 'W', 'K', r'$\Gamma$', 'L', 'U', 'W', 'L', 'K U', '', r'$\Gamma$'] # LaTeX
plt.xticks(kpoint_mappings, high_symmetry_kpoint_labels)

# Draw light vertical lines at high-symmetry points
for kpoint in kpoint_mappings:
    plt.axvline(kpoint, color='gray')

# Label axes
plt.xlabel(r'$\vec{k}$')
plt.ylabel(r'$\epsilon_i(\vec{k})$ [eV]')

# Set plot bounds (symmetric around Fermi energy)
plt.axis([kpoint_plotvalues[0], kpoint_plotvalues[-1], np.amin(bands), -np.amin(bands)])

# Plot and label Fermi energy
plt.axhline(0.0, color ='black', linestyle='--')
whitespace_shift = 0.01 * (kpoint_plotvalues[-1] - kpoint_plotvalues[0])
plt.text(kpoint_plotvalues[-1] + whitespace_shift, 0.0, r'$E_F$', verticalalignment='center')

# Set the plot title
plt.title('Kohn-Sham bands for fcc Cu using LDA-PZ exchange-correlation')

# Make the bands plot
for band_index in range(0, number_of_bands-1):
    plt.plot(kpoint_plotvalues, bands[band_index], color='green') # WARNING: ASSUMING BANDS ARE ORDERED BY ENERGY, SHOULD USE .RAP FILE
plt.show()


