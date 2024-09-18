## This script is used for writing the data in csv format

import csv
import json
import logging
from helpers.logging_client import LoggerManager

logging.getLogger("csv").setLevel(logging.ERROR)


def write_csv(
    logger_name,
    file_path,
    records,
    account,
    crontimeinhhmmss,
    header=None,
):
    """
    Responsible for writing given records to a CSV file at the given path.

    Parameters:
        - logger_name: Name of the logger (string).
        - file_path: Filesystem path where the final CSV/JSON file will be written (string).
        - records: Data to be written to the CSV/JSON (list or generator).
        - account: Account information (string).
        - crontimeinhhmmss: Cron time in hhmmss format (string).
        - header: The header row for the CSV (list of strings).
        - dry_run: If True, simulates writing the CSV without actually writing (boolean).
    """
    logger = LoggerManager.getLogger(logger_name, account, crontimeinhhmmss)
    if header:
        logger.info("Data must be in JSON and we want to write in CSV")
        with open(file_path, mode="w", newline="") as f:
            # Create a CSV DictWriter object
            writer = csv.DictWriter(f, fieldnames=header)
            # Write the header (column names)
            writer.writeheader()

            # Write the data rows
            writer.writerows(records)
            logger.info(f"---Data successfully written to {file_path}---")
    else:
        logger.info("Data writing in a JSON file")
        # Writing to the JSON file
        with open(file_path, "w") as f:
            json.dump(records, f)
        logger.info(f"Data successfully written to {file_path}")


def read_csv(
    file_path,
    logger_name,
    account,
    crontimeinhhmmss,
    encoding="utf8",
):
    """
    Reads the CSV file at the given file path and returns records.

    Parameters:
        - file_path: Filesystem path where the CSV file resides (string).
        - logger_name: Name of the logger (string).
        - account: Account information (string).
        - crontimeinhhmmss: Cron time in hhmmss format (string).
        - encoding: Encoding format for the CSV file (string, default 'utf8').

    Returns:
        - Generator yielding individual records (dict).
    """
    logger = LoggerManager.getLogger(logger_name, account, crontimeinhhmmss)
    logger.info("Reading from file at %s", file_path)

    try:
        with open(file_path, encoding=encoding) as csv_file:
            yield from csv.DictReader(csv_file)
    except IOError as e:
        logger.exception("I/O error: Unable to read data from CSV file: %s", e)
