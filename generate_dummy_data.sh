#!/bin/bash

# Bash script was written with ChatGPT

# Function to generate a random binary value (0 or 1)
generate_random_binary() {
    echo $((RANDOM % 2))
}

# Default number of rows and columns
default_rows=10000
default_columns=50

# Directory to write the file
output_directory="data"

# Check if the directory exists, if not, create it
if [[ ! -d "$output_directory" ]]; then
    mkdir -p "$output_directory"
fi

# Get user input for number of rows
read -p "Enter the number of rows, or participants (default: $default_rows): " user_rows
rows=${user_rows:-$default_rows}

# Get user input for number of columns
read -p "Enter the number of columns, or conditions (default: $default_columns): " user_columns
columns=${user_columns:-$default_columns}

# Generate header row
header="index"
for ((i=1; i<=$columns; i++)); do
    header+=$'\t'
    header+="disease_$i"
done

# Write header to file
echo "$header" > "$output_directory/dummy_data.tsv"

# Generate data rows
for ((j=1; j<=$rows; j++)); do
    row="$j"
    for ((k=1; k<=$columns; k++)); do
        row+=$'\t'
        row+="$(generate_random_binary)"
    done
    echo "$row" >> "$output_directory/dummy_data.tsv"
done

echo "Dummy data file generated: $output_directory/dummy_data.tsv"
