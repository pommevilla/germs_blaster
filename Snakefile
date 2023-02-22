configfile: "config.yml"
include: "rules/common.smk"

# Uploads a single BLAST results file to the MongoDB.
# Make sure to change the file path and project name in config.yml
rule upload_blast_results_file:
    input: 
        upload_script = "code/upload_one_to_mongodb.py"
    output: 
        f"outputs/{input_fasta}_mongodb.res"
    params:
        input_fasta_path = input_fasta_path,
        project_name = project_name
    log:
        err = "logs/upload_blast_results_file.err",
        out = "logs/upload_blast_results_file.out"
    conda:
        "environment.yml"
    shell:
        """
        {input.upload_script} -i {params.input_fasta_path} \
            -p {params.project_name} \
            2> {log.err} 1> {log.out}
        """

# Uploads a directory of BLAST results to the MongoDB
# Make sure to change the directory and project name in config.yml
rule upload_blast_results_directory:
    input: 
        upload_script = "code/upload_many_to_mongodb.py"
    output: 
        expand(
            "outputs/{input_fasta_file}_mongodb.res", 
            input_fasta_file=all_fasta_names
        )
    params:
        input_fasta_directory = input_fasta_directory,
        project_name = project_name
    log:
        err = "logs/upload_blast_results_directory.err",
        out = "logs/upload_blast_results_directory.out"
    conda:
        "environment.yml"
    shell:
        """
        {input.upload_script} -i {params.input_fasta_directory} \
            -p {params.project_name} \
            2> {log.err} 1> {log.out}
        """
