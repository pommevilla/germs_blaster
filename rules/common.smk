import os

## Globals
input_fasta_path = config["blast_results_file"]
input_fasta = os.path.basename(input_fasta_path)
project_name = config["project_name"]

input_fasta_directory = config["blast_results_directory"]
all_fasta_paths = os.listdir(input_fasta_directory)
all_fasta_names = [os.path.basename(file_path) for file_path in all_fasta_paths]