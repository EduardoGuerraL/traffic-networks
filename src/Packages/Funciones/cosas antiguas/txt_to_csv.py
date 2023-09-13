def read_data_from_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Parse the numbers from each line and store them in a tuple
            numbers = tuple(map(int, line.strip('()\n').split(',')))
            data.append(numbers)
    return data

def transpose_data(data):
    # Transpose the data to change rows into columns
    transposed_data = list(zip(*data))
    return transposed_data

def write_data_to_file(file_path, transposed_data):
    with open(file_path, 'w') as file:
        # Write the column names as the first row
        column_names = ["nodo"] + [f"{i * 10000}" for i in range(1, len(transposed_data[0]))]
        file.write(",".join(column_names) + "\n")
        
        # Write the transposed data to the file in the desired format
        for idx, row in enumerate(transposed_data):
            file.write(f"{idx}, {', '.join(str(num) for num in row)}\n")


if __name__ == "__main__":
    input_file = "SimpleNet_Ehr_10mA_500MT.txt"  # Replace this with the path to your input file
    output_file = "data/DataNetwork/StreetAsNode/txtes/SimpleNet_Ehr_10mA_500MT.csv"  # Replace this with the desired output file path

    # Read the data from the input file
    data = read_data_from_file(input_file)

    # Transpose the data
    transposed_data = transpose_data(data)

    # Write the transposed data to the output file
    write_data_to_file(output_file, transposed_data)