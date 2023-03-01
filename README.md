# GERMS BLASTER

Upload BLAST results to our database so that you can interact with them on the dashboard.

## Getting started

### Create your `.env` file 

1. Get access to the MongoDB database (ask Paul for help)
2. Create an `.env` file by copying and renaming `.env.example`.
3. Fill in your MongoDB password and username in `.env`. 
    * `.env` is under `gitignore`, so your private credentials won't be uploaded to git in the event you pushed to the repo. 

### Creating the conda environment

1. Install [conda](https://docs.conda.io/en/latest/), the Python package manager. I actually recommend using [mamba](https://github.com/mamba-org/mamba), but you can use whichever you like.
2. Create the environment by entering `conda env create -f environment.yml`. If you are using `mamba`, instead type `mamba env create -f environment.yml`. This will set up the virtual environment with all the required packages for the pipeline.

### Uploading BLAST results

1. Edit `config.yml`:
    * If you are uploading a single file, change the `blast_results_file` path to point to your file. 
    * If you are uploading a directory of BLAST results files, change the `blast_results_directory` path to point to your directory. 
    * Change `project_name` to whatever project you'd like these results to be under. This is just metadata to help other people search for these results. Some example values might be `LAMPS` or `CABBI` or `DNR_HABS`
2. Activate the virtual environment by typing `conda activate germs_blaster`. You should see `germs_blaster` appear on your command line somewhere, indicating that you are in that environment now.
3. You're ready to upload.
    * To upload a single file, type `snakemake -F upload_blast_results_file -c 1`
    * To upload a directory, use `snakemake -F upload_blast_results_directory`

After the records are uploaded, you'll see a `{file_name}_mongodb.res` file in the `outputs` directory  for each file you uploaded. This file contains some information about the run.

If there weren't any problems with the upload, the new data should be available on the [dashboard](https://pommevilla.shinyapps.io/main/) right away.

*Notes:*

* This pipeline assumes your BLAST results are in outfmt 6 without any modification.
* *Caution:* When uploading a directory of results, ensure that `blast_results_directory` contains *only* BLAST results files. Otherwise, the pipeline will crash.

## Planned features

For this backend helper:

- [ ] Submit fasta file for remote BLAST 
- [x] Upload BLAST results file 
- [ ] Allow any column headers

For the dashboard:

- [ ] Best *n* hits per query sequence
- [ ] Look up annotation info in nt/nr
- [ ] Downloadable reports

## Random notes

### To drop all files in the blast_results collection using MongoDB Compass

1. Connect to the database using MongoDB Compass
2. In mongosh, to set  `all_blast_results` as the working collection, type:
   * `use blast_results`
   * `db.all_blast_results` 
3. Enter `db.dropDatabase()` to remove all of the entries in the `all_blast_results` database.
