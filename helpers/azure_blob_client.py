#
#
#
#  Copyright (C) 2020 IHS Markit.
#  All Rights Reserved
#
#
#  NOTICE: All information contained herein is, and remains
#  the property of IHS Markit and its suppliers,
#  if any. The intellectual and technical concepts contained
#  herein are proprietary to IHS Markit and its suppliers
#  and may be covered by U.S. and Foreign Patents, patents in
#  process, and are protected by trade secret or copyright law.
#  Dissemination of this information or reproduction of this material
#  is strictly forbidden unless prior written permission is obtained
#  from IHS Markit.
#
#
#
import logging
import subprocess
from shutil import rmtree

from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError

from helpers.logging_client import LoggerManager

logging.getLogger("azure.storage.common").setLevel(logging.WARNING)
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)


class AzureBlobClient:
    def __init__(
        self,
        logger_name,
        account,
        crontimeinhhmmss,
        storage_account_key=None,
        storage_account_name=None,
        storage_account_url=None,
        container_name=None,
    ):
        """
        Constructor method which captures all the required information to
        make Azure blob connection.

        Parameters:
            - logger_name: Name of the logger (string).
            - account: Account information (string).
            - crontimeinhhmmss: Cron time in hhmmss format (string).
            - storage_account_key: Azure storage account key (string).
            - storage_account_name: Azure storage account name (string).
            - storage_account_url: Azure storage account URL (string).
            - container_name: Name of the Azure container (string).
        """
        self.storage_account_key = storage_account_key
        self.storage_account_name = storage_account_name
        self.storage_account_url = storage_account_url
        self.container_name = container_name

        self.conn = None
        self.blob_conn = None
        self.logger = LoggerManager.getLogger(logger_name, account, crontimeinhhmmss)
        self.conn = self.get_connection()
        self.create_container(self.container_name)

    def get_connection(self):
        """
        Establishes connection to Azure Blob service.

        Returns:
            - BlobServiceClient: Connection to Azure Blob service.
        """
        if not self.conn:
            self.logger.info(
                "Establishing connection to Azure Blob using account name: %s",
                self.storage_account_name,
            )
            try:
                self.conn = BlobServiceClient(
                    account_url=self.storage_account_url,
                    credential=self.storage_account_key,
                )
                self.logger.info("Connection successful to blob")
            except Exception as e:
                self.logger.exception(
                    "ERROR: An error in connecting to the Azure Blob: %s",
                    str(e),
                )
        return self.conn

    def create_container(self, container_name):
        """
        Creates an Azure Blob container if it does not already exist.

        Parameters:
            - container_name: Name of the container to create (string).

        Returns:
            - container_name: The name of the created or existing container.
        """
        try:
            self.conn.create_container(name=container_name)
            self.logger.info("Container %s has been created.", container_name)
        except ResourceExistsError:
            self.logger.info(
                "The container with the given name: %s already exists."
                " Not creating again.",
                container_name,
            )
        return container_name

    def download_file(self, down_container_name, down_blob_name, down_file_path):
        """
        Downloads a file from Azure Blob storage to the local system.

        Parameters:
            - down_container_name:
                Name of the container from which to download.
            - down_blob_name:
                Name of the blob to download (string).
            - down_file_path:
                Local file path to save the downloaded file (string).
        """
        blob_conn = self.conn.get_blob_client(
            container=down_container_name, blob=down_blob_name
        )
        with open(down_file_path, "wb") as my_blob:
            download_stream = blob_conn.download_blob()
            my_blob.write(download_stream.readall())
        self.logger.info("Downloaded the file from blob - %s", down_blob_name)

    def upload_file(self, container_name, blob_name, file_path):
        """
        Uploads a file from the local system to Azure Blob storage.

        Parameters:
            - container_name: Name of the container to upload to (string).
            - blob_name: Name of the blob to create (string).
            - file_path: Local file path of the file to upload (string).
        """
        self.blob_conn = self.conn.get_blob_client(
            container=container_name, blob=blob_name
        )
        with open(file_path, "rb") as data:
            self.blob_conn.upload_blob(data, overwrite=True)
        self.logger.info("Uploaded the file into blob - %s", blob_name)

    def cleanup(self, dir_path):
        """
        Deletes the local directory and its contents.

        Parameters:
            - dir_path: Path to the directory to delete (string).
        """
        self.logger.info("Removing folder at %s", dir_path)
        rmtree(dir_path, ignore_errors=True)
