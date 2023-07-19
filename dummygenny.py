import csv
import random
import datetime
import os


def generate_dummy_data():
    try:
        num_columns = get_valid_integer_input("Enter the number of columns (index column provided automatically): ")
        num_data = get_valid_integer_input("Enter the number of data to generate: ")

        column_names = ['No.']
        column_data_types = ['index']
        column_ranges = {}

        # Get column names and data types
        for _ in range(num_columns):
            name = get_valid_input("Enter column name: ", "Column name cannot be blank. Please enter a valid name.")
            column_names.append(name)

            data_type = get_valid_data_type_input(f"Enter data type for column '{name}' (1. integer, 2. date, or 3. string): ")
            column_data_types.append(data_type)

            if data_type == "date" or data_type == '2':
                date_range_input = input(f"Enter date range for column '{name}' (DD/MM/YYYY to DD/MM/YYYY): ")
                if date_range_input:
                    start_date, end_date = map(str.strip, date_range_input.split("to"))
                    column_ranges[name] = (datetime.datetime.strptime(start_date, "%d/%m/%Y").date(),
                                            datetime.datetime.strptime(end_date, "%d/%m/%Y").date())
            elif data_type == "string" or data_type == '3':
                file_path = input(f"Enter .csv file path for column '{name}' data content (leave blank if there is none): ")
                if file_path:
                    with open(file_path, "r") as file:
                        reader = csv.reader(file)
                        column_ranges[name] = [row[0] for row in reader if row]

            elif data_type == "integer" or data_type == '1':
                number_range_input = input(f"Enter number range for column '{name}' (start to end): ")
                if number_range_input:
                    start_num, end_num = map(int, number_range_input.split("to"))
                    column_ranges[name] = (start_num, end_num)

        # Generate dummy data
        data = []
        for i in range(num_data):
            row = []
            for j in range(len(column_names)):
                data_type = column_data_types[j]
                name = column_names[j]
                if data_type == "index":
                    row.append(str(i + 1))
                elif data_type == "date":
                    start_date, end_date = column_ranges.get(name, (datetime.date.min, datetime.date.max))
                    random_date = random_date_in_range(start_date, end_date)
                    row.append(random_date.strftime("%d/%m/%Y"))
                elif data_type == "string":
                    values = column_ranges.get(name, [])
                    if values:
                        row.append(random.choice(values))
                    else:
                        row.append(generate_random_word())
                elif data_type == "integer":
                    start_num, end_num = column_ranges.get(name, (0, 100))
                    row.append(str(random.randint(start_num, end_num)))
            data.append(row)

        # Save data to CSV file
        file_name = "dummy_data.csv"
        if os.path.exists(file_name):
            os.remove(file_name)
        with open(file_name, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(column_names)
            writer.writerows(data)

        print(f"Dummy data generated and saved to {file_name}.")
    except ValueError as e:
        print("Invalid input:", str(e))
        generate_dummy_data()


def get_valid_input(prompt, error_message):
    value = input(prompt)
    while not value:
        print(error_message)
        value = input(prompt)
    return value


def get_valid_integer_input(prompt):
    while True:
        value = input(prompt)
        try:
            value = int(value)
            if value <= 0:
                print("Number must be greater than 0.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_valid_data_type_input(prompt):
    valid_data_types = ["integer", "date", "string", "1", "2", "3"]
    while True:
        value = input(prompt)
        if value not in valid_data_types:
            print("Invalid input. Please enter a valid data type (integer, date, or string).")
        else:
            return value


def random_date_in_range(start_date, end_date):
    delta = end_date - start_date
    random_days = random.randint(0, delta.days)
    return start_date + datetime.timedelta(days=random_days)


def generate_random_word(length=8):
    letters = "abcdefghijklmnopqrstuvwxyz"
    return "".join(random.choice(letters) for _ in range(length))


if __name__ == "__main__":
    generate_dummy_data()
