#!/usr/bin/env python
# ---------------------------
# Uploads all the BLAST results in a directory to MongoDB
# Author: Paul Villanueva (github.com/pommevilla)
# ---------------------------
from typing import Collection
from dotenv import dotenv_values
import pymongo
from os.path import join
from os import listdir
from upload_one_to_mongodb import upload_blast_results_to_mongodb


def upload_blast_results_directory_to_mongodb(
    input_file_directory: str, project_name: str, mongodb_collection: Collection
):
    """
    Upload all BLAST results files in a directory to the MongoDB.
    This is a thin wrapper over upload_blast_results_to_mongodb
    """
    for file in listdir(input_file_directory):
        this_file_path = join(input_file_directory, file)
        upload_blast_results_to_mongodb(
            input_file_path=this_file_path,
            project_name=project_name,
            mongodb_collection=mongodb_collection,
        )


def main(args):
    """
    Parses arguments and passes them to the driver function
    """

    # Reading config values
    fasta_directory = args.fasta_directory
    project_name = args.project_name

    # MongoDB Connection
    config = dotenv_values(".env")
    MONGODB_URI = config["MONGODB_URI"]
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.blast_results
    all_blast_results = db["all_blast_results"]

    upload_blast_results_directory_to_mongodb(
        input_file_directory=fasta_directory,
        project_name=project_name,
        mongodb_collection=all_blast_results,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Upload a single BLAST results file to MongoDB"
    )
    parser.add_argument(
        "-i",
        dest="fasta_directory",
        help="the input file to upload to MongoDB",
    )
    parser.add_argument(
        "-p", dest="project_name", help="the name of the associated project"
    )

    args = parser.parse_args()

    main(args)
