import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt

convergence_threshold = 7.35e-5     #this is = 1meV
etot = np.array([-28.62713789, -28.6287778, -28.62919416, -28.62932407, -28.629335245, -28.62936495,
                 -28.62937577, -28.62937672, -28.6293831, -28.62938387, -28.62938475, -28.629384793, -28.62938558])
ecut = np.array([30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150])

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

# plt.savefig('Cu.Fm-3m.PBEsol.KJPAW.ecut_etotal.png')


# -28.53478791


# 18pt serif font (use latex)
# math variables itlicized

# 'r' before string

# rotate the y-axis labels

# convert to delta E instead of Etotal
