import csv
import random

def add_random_integer(input_file, output_file):
    # Read the data from the input CSV file and store it in a list
    data_list = []
    with open(input_file, "r") as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Skip the header row
        for row in csv_reader:
            data_list.append(row)

    # Add a random integer between 1 and 100 as the last item of each row
    for row in data_list:
        random_int = random.randint(1, 100)
        row.append(random_int)

    # Write the modified data to a new CSV file
    with open(output_file, "w", newline="") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(header)  # Write the header row
        csv_writer.writerows(data_list)

# Example usage:
input_csv_file = "stockdata.csv"
output_csv_file = "new.csv"
add_random_integer(input_csv_file, output_csv_file)