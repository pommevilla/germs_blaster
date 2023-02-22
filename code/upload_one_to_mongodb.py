#!/usr/bin/env python
# ---------------------------
# Takes a BLAST results file and pushes it to the MongoDB
# Author: Paul Villanueva (github.com/pommevilla)
# ---------------------------
from typing import Collection, List, Dict
from dotenv import dotenv_values
import pymongo
from os.path import basename

mongodb_column_names = [
    "qseqid",
    "sseqid",
    "pident",
    "length",
    "mismatch",
    "gapopen",
    "qstart",
    "qend",
    "sstart",
    "send",
    "evalue",
    "bitscore",
    "file_name",
    "project_name",
]


def create_mongodb_entry_from_line(
    blast_result_line: List[str],
    column_names: List[str] = mongodb_column_names,
) -> Dict[str, str]:
    """
    Creates a single MongoDB entry from a BLAST results line (with
    additional metadata)
    """
    return {k: v for k, v in zip(column_names, blast_result_line)}


def upload_blast_results_to_mongodb(
    input_file_path: str, project_name: str, mongodb_collection: Collection
):
    """
    Uploads a file of BLAST results to the MongoDB
    """
    input_file = basename(input_file_path)

    new_entries = []
    with open(input_file_path) as fin:
        for line in fin:
            new_line = line.strip().split() + [input_file, project_name]
            new_mongo_entry = create_mongodb_entry_from_line(new_line)
            new_entries.append(new_mongo_entry)

    results = mongodb_collection.insert_many(new_entries)

    num_records = len(results.inserted_ids)
    output_file_name = f"outputs/{input_file}_mongodb.res"

    with open(output_file_name, "w") as fout:
        fout.write(f"Input file: {input_file_path}\n")
        fout.write(f"Successfully uploaded {num_records} new records.\n")
        fout.write("Inserted IDS:\n")
        for id in results.inserted_ids:
            fout.write(f"\t{id}\n")


def main(args):
    """
    Parses arguments and passes them to the driver function
    """

    # Arguments from config.yml
    input_file_path = args.input_fasta_file_path
    project_name = args.project_name

    # Connect to the MongoDB
    config = dotenv_values(".env")
    MONGODB_URI = config["MONGODB_URI"]
    client = pymongo.MongoClient(MONGODB_URI)
    db = client.blast_results
    all_blast_results = db["all_blast_results"]

    print(f"{input_file_path=}")
    print(f"{project_name=}")

    upload_blast_results_to_mongodb(
        input_file_path=input_file_path,
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
        dest="input_fasta_file_path",
        help="the input file to upload to MongoDB",
    )
    parser.add_argument(
        "-p", dest="project_name", help="the name of the associated project"
    )

    args = parser.parse_args()

    main(args)
