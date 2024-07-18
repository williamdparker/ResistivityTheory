import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib


matplotlib.use('macosx')

electricaldatatable = pd.read_html("https://www.angstromsciences.com/elements-electrical-conductivity")[0]
thermaldatatable = pd.read_html("https://www.angstromsciences.com/thermal-conductivity-of-elements")[0]

print(thermaldatatable)


electricaldatatable['Electrical Conductivity'] = electricaldatatable['Electrical Conductivity'].str.split().str[0]
thermaldatatable['Thermal Conductivity'] = thermaldatatable['Thermal Conductivity'].str.split().str[0]
completedatatable = []
remove = [1, 2]
electricaldatatable = electricaldatatable.to_numpy()
electricaldatatable = np.delete(electricaldatatable, remove, axis=1)
thermaldatatable = thermaldatatable.to_numpy()
thermaldatatable = np.delete(thermaldatatable, remove, axis=1)
electricaldatatable = np.fliplr(electricaldatatable)
thermaldatatable = np.fliplr(thermaldatatable)
sorted = np.argsort(electricaldatatable[:, 0])
electricaldatatable = electricaldatatable[sorted]
sorted = np.argsort(thermaldatatable[:, 0])
thermaldatatable = thermaldatatable[sorted]
#print(electricaldatatable)
#print(thermaldatatable)
#for x in thermaldatatable[:, 0]:
#    addrow = [x, thermaldatatable[x, 1], electricaldatatable[x, 1]]
#    completedatatable = numpy.vstack([completedatatable, ])
#    print(electricaldatatable[x, 0])
#    print(addrow)
# for x in thermaldatatable[:, 0]:
#     if thermaldatatable[x, 0] == electricaldatatable[x, 0]:
#         addrow = [x, thermaldatatable[x, 1], electricaldatatable[x, 1]]
#        print(addrow)
#conductivities = {}

#for atomic_number in range(1, 105):
#    for atomic_number_inside, electrical_conductivity in electricaldatatable:
#        if int(atomic_number_inside) == atomic_number:
#            conductivities[atomic_number] = {'electrical conductivity': electrical_conductivity}
#    for atomic_number_inside, thermal_conductivity in thermaldatatable:
#        if int(atomic_number_inside) == atomic_number:
#            if int(atomic_number_inside) in conductivities.keys():
#                conductivities[atomic_number]['thermal conductivity'] == thermal_conductivity
#            else:
#                conductivities[atomic_number] = {'thermal conductivity': thermal_conductivity}
#print(conductivities)
for X in range(0, 104):
    for Y in range(0, 78):
        if thermaldatatable[X, 0] == electricaldatatable[Y, 0]:
            conductivitytemp = [int(thermaldatatable[X, 0]), float(thermaldatatable[X, 1])*1e2, float(electricaldatatable[Y, 1])/1e8]
            completedatatable.append(conductivitytemp)
        else:
            pass
completedatatable = np.array(completedatatable)
# print(completedatatable)

atomic_numbers = completedatatable.transpose()[0]
thermal_conductivities = completedatatable.transpose()[1]
electrical_conductivities = completedatatable.transpose()[2]

plt.plot(thermal_conductivities, electrical_conductivities, marker='o', linestyle='', markersize=4)

for atomic_number, thermal, electrical in zip(atomic_numbers, thermal_conductivities, electrical_conductivities):
    if electrical < 1e-11:
        plt.text(thermal, electrical, int(atomic_number), ha='center', va='bottom')

#print(completedatatable.transpose()[1])
#plt.plot(completedatatable.transpose()[1], completedatatable.transpose()[2], marker='o', linestyle='')

plt.xscale('log')
plt.yscale('log')

plt.xlabel(r'$\kappa$ [W/(m K)]')
plt.ylabel(r'$\sigma$ [S/m]')

plt.show()