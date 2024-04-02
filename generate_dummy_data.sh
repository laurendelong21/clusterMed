#!/bin/bash

# Bash script was written with ChatGPT

# Function to generate a random binary value (0 or 1)
generate_random_binary() {
    echo $((RANDOM % 2))
}

# Number of rows and columns
rows=10000
columns=50

# Directory to write the file
output_directory="data"

# Check if the directory exists, if not, create it
if [[ ! -d "$output_directory" ]]; then
    mkdir -p "$output_directory"
fi

# Generate header row
header=""
for ((i=1; i<=$columns; i++)); do
    header+="disease_$i"
    if [[ $i -ne $columns ]]; then
        header+=$'\t'
    fi
done

# Write header to file
echo "$header" > "$output_directory/dummy_data.tsv"

# Generate data rows
for ((j=1; j<=$rows; j++)); do
    row=""
    for ((k=1; k<=$columns; k++)); do
        row+="$(generate_random_binary)"
        if [[ $k -ne $columns ]]; then
            row+=$'\t'
        fi
    done
    echo "$row" >> "$output_directory/dummy_data.tsv"
done

echo "Dummy data file generated: $output_directory/dummy_data.tsv"