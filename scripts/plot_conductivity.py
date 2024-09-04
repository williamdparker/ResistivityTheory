import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform


def setup_backend():
    if platform.system() == "Darwin":
        import matplotlib
        matplotlib.use('macosx')


def get_data():
    from import_data_from_csv import import_csv_data

    if platform.system() == "Windows":
        thermal_data = import_csv_data(
            r"C:\Users\Owner\PycharmProjects\ResistivityTheory\inputs\Thermal_Conductivity.csv")
        electrical_data = import_csv_data(
            r"C:\Users\Owner\PycharmProjects\ResistivityTheory\inputs\Electrical_Conductivity.csv")
    else:
        # thermal_data = import_csv_data("../inputs/Electrical_Conductivity.csv")
        thermal_data = []
        import csv
        with open('../inputs/Thermal_Conductivity.csv') as csv_file:
            file_reader = csv.reader(csv_file)
            next(file_reader)
            for row in file_reader:
                thermal_data.append([float(row[0]), row[1], int(row[2])])

        # electrical_data = import_csv_data("../inputs/Thermal_Conductivity.csv")
        electrical_data = []
        import csv
        with open('../inputs/Electrical_Conductivity.csv') as csv_file:
            file_reader = csv.reader(csv_file)
            next(file_reader)
            for row in file_reader:
                electrical_data.append([float(row[0]), row[1], int(row[2])])

    # print('Thermal Conductivities')
    # print(thermal_data)
    # print()
    # print('Electrical Conductivities')
    # print(electrical_data)
    # print()

    return thermal_data, electrical_data


def sort_data(thermal_data_table, electrical_data_table):
    data_tables = []
    for data_table in thermal_data_table, electrical_data_table:
        sorted_data_table = np.argsort([pair[0] for pair in data_table])
        temporary_list = []
        for atomic_number_index in sorted_data_table:
            temporary_list.append(data_table[atomic_number_index])
        data_tables.append(np.array(temporary_list))

    return data_tables[0], data_tables[1]


def combine_data(thermal_data_table, electrical_data_table):
    complete_data_table = []
    for X in range(len(thermal_data_table)):
        for Y in range(len(electrical_data_table)):
            if thermal_data_table[X, 2] == electrical_data_table[Y, 2]:
                conductivity_temporary = [
                    int(thermal_data_table[X, 2]),
                    float(thermal_data_table[X, 0]) * 1e2,
                    float(electrical_data_table[Y, 0]) / 1e8,
                    str(thermal_data_table[X, 1])
                ]
                complete_data_table.append(conductivity_temporary)
            else:
                pass

    complete_data_table = np.array(complete_data_table, dtype=object)

    atomic_numbers = complete_data_table.transpose()[0]
    thermal_conductivities = complete_data_table.transpose()[1]
    electrical_conductivities = complete_data_table.transpose()[2]
    atomic_symbols = complete_data_table.transpose()[3]

    return atomic_numbers, thermal_conductivities, electrical_conductivities, atomic_symbols


def plot_data(atomic_numbers, thermal_conductivities, electrical_conductivities, atomic_symbols):
    S_Block = [3, 4, 11, 12, 19, 20, 37, 38, 55, 56, 87, 88]  # Red
    P_Block = [5, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 18, 31, 32, 33, 34, 35, 36, 49, 50, 51, 52, 53, 54, 81, 82, 83,
               84, 85, 86]  # Blue
    D_Block = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 71, 72, 73, 74, 75, 76,
               77, 78, 79, 80]  # Green
    F_Block = [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 89, 90, 91, 92, 93, 94]  # Orange

    # print(electrical_conductivities)
    # plt.plot(thermal_conductivities, electrical_conductivities, marker='o', linestyle='', markersize=4)

    maximum_electrical_element = [1, 0, 0, 'X']
    minimum_thermal_element = [1, np.max(thermal_conductivities), 0, 'X']
    for atomic_number, thermal, electrical, symbol in \
            zip(atomic_numbers, thermal_conductivities, electrical_conductivities, atomic_symbols):
        if electrical > maximum_electrical_element[2]:
            maximum_electrical_element = [atomic_number, thermal, electrical, symbol]
        if electrical < 1e-11:
            plt.text(thermal, electrical*2, symbol, ha='center', va='bottom')
        else:
            if thermal < minimum_thermal_element[1]:
                minimum_thermal_element = [atomic_number, thermal, electrical, symbol]

    plt.text(maximum_electrical_element[1], maximum_electrical_element[2]*0.5, maximum_electrical_element[3],
             ha='center', va='top')
    plt.text(minimum_thermal_element[1], minimum_thermal_element[2]*20, minimum_thermal_element[3],
             ha='center', va='top')


    for atomic_number, thermal, electrical in \
            zip(atomic_numbers, thermal_conductivities, electrical_conductivities):
        if atomic_number in S_Block:
            plt.plot(thermal, electrical, color='red', marker='o', linestyle='', markersize=4)
        elif atomic_number in P_Block:
            plt.plot(thermal, electrical, color='blue', marker='o', linestyle='', markersize=4)
        elif atomic_number in D_Block:
            plt.plot(thermal, electrical, color='green', marker='o', linestyle='', markersize=4)
        elif atomic_number in F_Block:
            plt.plot(thermal, electrical, color='orange', marker='o', linestyle='', markersize=4)

    plt.xscale('log')
    plt.yscale('log')

    plt.xlabel(r'$\kappa$ [W/(m K)]')
    plt.ylabel(r'$\sigma$ [S/m]')
    plt.savefig("plot_conductivity.png")
    plt.show()


if __name__ == '__main__':
    setup_backend()
    data = get_data()
    sorted_data = sort_data(data[0], data[1])
    combined_data = combine_data(sorted_data[0], sorted_data[1])
    plot_data(combined_data[0], combined_data[1], combined_data[2], combined_data[3])
