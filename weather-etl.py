## This is the Main ETL python script


from helpers.azure_blob_client import AzureBlobClient
from helpers.create_file_helper import write_csv
from helpers.logging_client import LoggerManager
from helpers.weather_client import WeatherClient

import configparser
import logging
import os
import sys
from datetime import datetime
import socket
import platform
from uuid import uuid4

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(SCRIPT_DIR)


logging.getLogger("azure.storage.common").setLevel(logging.ERROR)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)


class ETL:
    def __init__(self, crontimeinhhmmss):
        """
        Constructor method
        """
        self.crontimeinhhmmss = crontimeinhhmmss

    def run(self):
        self.read()
        self.create()
        self.load()

    def read(self):
        """
        Reads the config file to get information about the environment,
        account, and other necessary parameters.
        """
        config = configparser.ConfigParser()
        config.read("config.ini")

        self.account = config["environment"]["account"]
        self.dry_run = config["environment"]["dry_run"]

        self.logger_name = "weather"
        self.logger, self.log_location = LoggerManager.getLogger(
            self.logger_name, self.account, self.crontimeinhhmmss, location=True
        )

        self.azure_blob_conn_params = config[f"azure_blob_{self.account}"]
        self.azure_blob_conn_params["logger_name"] = self.logger_name
        self.azure_blob_conn_params["account"] = self.account
        self.azure_blob_conn_params["crontimeinhhmmss"] = self.crontimeinhhmmss

        self.weather_client_params = config["weather_creds"]
        self.weather_client_params["logger_name"] = self.logger_name
        self.weather_client_params["account"] = self.account
        self.weather_client_params["crontimeinhhmmss"] = self.crontimeinhhmmss

        self.csv_config = config["csv_config"]
        self.write_csv = self.csv_config.get("write_csv", "False") == "True"
        self.csv_file_path = self.csv_config.get("csv_file_path", "")

        self.start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    def create(self):
        """
        Initiate the connection for Azure table,
        Azure blob and other clients
        Returns:
            - None
        """
        self.azure_blob_client = AzureBlobClient(**self.azure_blob_conn_params)
        self.weather_client = WeatherClient(**self.weather_client_params)

    def load(self):
        """
        Loads data and uploads it to Azure Table and Azure Blob.
        """
        os.makedirs("files", exist_ok=True)  # To store data locally first
        dry_run_mode = True if self.dry_run.lower() == "true" else False
        if dry_run_mode:
            self.logger.info("******* THIS JOB IS BEING RUN IN A DRY RUN MODE *******")
        
        exceptions = list()
        weather_data, status, exception_string = self.weather_client.get_weather_data()
        try:
                self.upload_azure(weather_data, "weather")
                status = "SUCCESS"
        except Exception as e:
                self.loger.exception(e.args)
                status = "FAIL"
                exceptions.append(str(e))
        
        if self.dry_run.lower() == "false":
            self.cleanup()
        else:
            print(
                "***** Not removing locally files, As it is runnning in dry mode *****"
            )
        
    def upload_files_from_dir(
        self, container_name, dir_path, table_name, file_extension
    ):
        """
        Uploads files from a directory to Azure Blob.
        """
        if os.listdir(dir_path):
            for file in os.listdir(dir_path):
                self.azure_blob_client.upload_file(
                    container_name, f"{table_name}/{file}", f"{dir_path}/{file}"
                )
                self.azure_blob_client.upload_file(
                    container_name,
                    f"{table_name}/latest.{file_extension}",
                    f"{dir_path}/{file}",
                )
        else:
            print("No files found to upload")
            self.logger.info("No files found to upload")

    def upload_azure(self, records, table_name):
        """
        Parameters:
            - argument 1: records: List of data that has to be uploaded
            - argument 2: table_name: Name in the Azure table and Blob
        Return:
             -None
        """

        self.logger.info("Length of records is: %s" % len(records))
        if self.dry_run.lower() == "true":
            print("******* Code running in dry run mode *******")
            self.logger.info("******* Code running in dry run mode *******")
        try:
            if records:
                # Write today's data into csv file.
                if self.write_csv and self.csv_file_path:

                    file_extension = "csv"
                    # in case if we want to convert JSON into CSV
                    headers = (
                        records[0].keys()
                        if file_extension == "csv"
                        and isinstance(records, list)
                        and records
                        and isinstance(records[0], dict)
                        else None
                    )
                    file_name = (
                        f"{datetime.now().strftime('%d.%m.%Y')}_"
                        f"{self.azure_blob_client.container_name}."
                        f"{table_name}.{file_extension}"
                    )
                    self.path = "{}/{}/{}".format(
                        self.csv_file_path, table_name, file_name
                    )
                    os.makedirs(f"{self.csv_file_path}/{table_name}", exist_ok=True)

                    # when we want to write csv
                    write_csv(
                        self.logger_name,
                        account=self.account,
                        crontimeinhhmmss=self.crontimeinhhmmss,
                        file_path=self.path,
                        records=records,
                        header=headers,
                    )
                container_name = self.azure_blob_client.create_container(
                    container_name=self.azure_blob_client.container_name
                )
                if self.dry_run.lower() == "false":
                    self.upload_files_from_dir(
                        container_name,
                        f"{self.csv_file_path}/{table_name}",
                        table_name,
                        file_extension,
                    )
            else:
                self.logger.info(f"There are no records for the table - {table_name}")

        except Exception as e:
            self.logger.exception(e.args)
            print(e.args)

    def cleanup(self):
        """
        Responsible for cleaning up the connections and resources
        """
        self.azure_blob_client.cleanup(self.csv_file_path)


def lambda_handler(event, context):
    print("start")
    current_time = datetime.now().strftime("%X")
    crontimeinhhmmss = current_time.replace(":", "")
    e = ETL(crontimeinhhmmss)
    e.run()
    print("Inserted the records into the table\n end")


if __name__ == "__main__":
    lambda_handler(event={}, context={})
