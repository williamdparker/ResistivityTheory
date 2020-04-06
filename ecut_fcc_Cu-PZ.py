import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

convergence_threshold = 7.35e-5     #this is = 1meV
etot = np.array([-187.76560276, -207.62934817, -207.97470798, -207.97753118, -207.98013155, -207.98011167,
                 -207.98035218, -207.98042862, -207.98042833])
ecut = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90])

plt.plot(ecut, etot, label='Total energy')
plt.scatter(ecut, etot)
# plt.title("Cutoff Energy vs Total Energy for PBESOL psuedopotential of Cu")
plt.xlabel("Cutoff Energy (Ry)")
plt.ylabel("Total Energy (meV/atom)")
plt.axhline(etot[-1], color='r', label='convergence energy')
plt.axhline(etot[-1]-convergence_threshold, color='r', linestyle='--', label='convergence threshold')
plt.axhline(etot[-1]+convergence_threshold, color='r', linestyle='--')
plt.text(130, etot[-1] + convergence_threshold*2, '+/- 1 meV')


# plt.legend()
# plt.axis([0, ecut[-1],etot[-1]-10*convergence_threshold, etot[-1]+10*convergence_threshold])
plt.show()

# plt.savefig('Cu.Fm-3m.PZ.KJPAW.ecut_etotal.png')


# -28.53478791


# 18pt serif font (use latex)
# math variables itlicized

# 'r' before string

# rotate the y-axis labels

# convert to delta E instead of Etotal
