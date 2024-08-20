def import_csv_data(csv_file):
    import csv

    # Path to your CSV file
    csv_file = 'data.csv'

    # Initialize an empty list to store the dictionaries
    data_list = []

    # Read the CSV file and convert each row into a dictionary
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data_list.append(dict(row))

    return data_list


if __name__ == '__main__':
    data_files = ['Electrical_Conductivity.csv', 'Thermal_Conductivity.csv']
    for file in data_files:
        print(import_csv_data(file))