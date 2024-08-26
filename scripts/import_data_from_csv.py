def import_csv_data(csv_file):
    import csv

    # Path to your CSV file
#    csv_file = 'data.csv'

    # Initialize an empty list to store the dictionaries
    data_list = []

    # Read the CSV file and convert each row into a dictionary
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        file.readline()
        for line in file:
#            print(line.split(','))
            conductivity = float(line.split(',')[0])
#            print(conductivity)
            if len(line.split(',')[-1]) > 2:
                atomicnumber = line.split(',')[-1][:-2]
            else:
                atomicnumber = line.split(',')[-1]
            data_list.append([int(atomicnumber), conductivity])
#        reader = csv.DictReader(file)
#        for row in reader:
#            data_list.append(dict(row))

    return data_list


if __name__ == '__main__':
    data_files = [r"C:\Users\Owner\PycharmProjects\ResistivityTheory\inputs\Thermal_Conductivity.csv",
                  r"C:\Users\Owner\PycharmProjects\ResistivityTheory\inputs\Electrical_Conductivity.csv"]
    for file in data_files:
        print(import_csv_data(file))