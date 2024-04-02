# A Systematic Clustering Analysis

This is the code repository corrresponding to the systematic clustering analysis within [TODO add preprint](https://laurendelong21.github.io/).

To begin, create a Python environment and install the package:

## Installation

Go to the repository:

    cd mrc_clustering

create and activate a Python environment (replace `$ENV_NAME$` with your desired environment name):

    python3 -m venv $ENV_NAME$
    source $ENV_NAME$/bin/activate


 and install the `clustr` package:

    pip install .


<br>

## Usage

<br>

### File format

This package operates upon [tab-separated files](https://en.wikipedia.org/wiki/Tab-separated_values) (.tsv).

- The column names should indicate the conditions.

- The rows should denote participants. The first column should be the patient ID (or some generic index number).

    - (In [pandas](https://pandas.pydata.org/), this would be the following):

          pd.read_csv(input_file, sep='\t', index_col=0)

The multimorbidity data should be binary (zero or one) indicating whether each participant (row) has a condition (row).

<br>

### Tutorial

[tutorial.ipynb](https://github.com/laurendelong21/mrc_clustering/tutorial.ipynb) gives an overview of how you can use the `clustr` package within your Python code.

To run the notebook, you need to do a few things first. First, create a dummy file by running [generate_dummy_data.sh](https://github.com/laurendelong21/mrc_clustering/generate_dummy_data.sh). 

Assuming you're already in the repository's directory,

    cd mrc_clustering

Run the script in the terminal. It will take a few minutes to generate a dummy file with 10,000 faux participants and 50 condition columns.

    ./generate_dummy_data.sh


Finally, connect your virtual environment as a kernel. Depending upon what you're using (Jupyter notebook, VSCode, etc.), there are various instructions online for doing so.

Using your environment as the kernel, use the notebook. Be careful with changing the proportion of the file used- these methods can be computationally expensive with large files, so consider whether your machine can handle working with the whole dummy file.

<br>

### Command Line Interface (CLI)

These clustering methods can be computationally expensive for many participants and conditions. You may want to run these on a remote server with a CLI.

To use the CLI,