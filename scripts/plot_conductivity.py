import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

electricaldatatable = pd.read_html("https://www.angstromsciences.com/elements-electrical-conductivity")[0]
thermaldatatable = pd.read_html("https://www.angstromsciences.com/thermal-conductivity-of-elements")[0]


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

# print(electricaldatatable)
# print(thermaldatatable)
#for x in thermaldatatable[:, 0]:
#    addrow = [x, thermaldatatable[x, 1], electricaldatatable[x, 1]]
#    completedatatable = numpy.vstack([completedatatable, ])
#    print(electricaldatatable[x, 0])
#    print(addrow)
# for x in thermaldatatable[:, 0]:
#     if thermaldatatable[x, 0] == electricaldatatable[x, 0]:
#         addrow = [x, thermaldatatable[x, 1], electricaldatatable[x, 1]]
#         print(addrow)

conductivities = {}

for atomic_number in range(1, 105):
    # electrical = False
    # thermal = False
    for atomic_number_inside, electrical_conductivity in electricaldatatable:
        if int(atomic_number_inside) == atomic_number:
            conductivities[atomic_number] = {'electrical conductivity': electrical_conductivity}
    for atomic_number_inside, thermal_conductivity in thermaldatatable:
        if int(atomic_number_inside) == atomic_number:
            if int(atomic_number_inside) in conductivities.keys():
                conductivities[atomic_number]['thermal conductivity'] == thermal_conductivity
            else:
                conductivities[atomic_number] = {'thermal conductivity': thermal_conductivity}


print(conductivities)


