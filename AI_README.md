
# AI Generated Project Title

## Description

This project is an ETL pipeline for weather data into Azure Blob Storage.
It includes the following components:

### ./weather-etl.py
Constructor method

- **__init__(self, crontimeinhhmmss)**: Constructor method

- **run(self):
        self.read()
        self.create()
        self.load()

    def read(self)**: Reads the config file to get information about the environment,
        account, and other necessary parameters.

- **create(self)**: Initiate the connection for Azure table,
        Azure blob and other clients
        Returns:
            - None

- **load(self)**: Loads data and uploads it to Azure Table and Azure Blob.

- **upload_files_from_dir(
        self, container_name, dir_path, table_name, file_extension
    )**: Uploads files from a directory to Azure Blob.

- **upload_azure(self, records, table_name)**: Parameters:
            - argument 1: records: List of data that has to be uploaded
            - argument 2: table_name: Name in the Azure table and Blob
        Return:
             -None

- **cleanup(self)**: Responsible for cleaning up the connections and resources

### ./generate_readme.py
This project is an ETL pipeline for weather data into Azure Blob Storage.
It includes the following components:

### ./helpers/weather_client.py
Initializes the DummyAPIClient with user credentials and logging setup.

        Parameters:
            - api_key: The API key for getting the weather data.
            - weather_url: The URL of the weather API.
            - lat: Latitude.
            - lon: Longitude.
            - units: Units of measurement (e.g., metric(for Celcius), imperial(for Farenheit))
            - logger_name: Name of the logger.
            - account: Account information.
            - crontimeinhhmmss: Cron time in hhmmss format.

- **__init__(
        self, api_key, weather_url, lat, lon, units, logger_name, account, crontimeinhhmmss, **kwargs
    )**: Initializes the DummyAPIClient with user credentials and logging setup.

        Parameters:
            - api_key: The API key for getting the weather data.
            - weather_url: The URL of the weather API.
            - lat: Latitude.
            - lon: Longitude.
            - units: Units of measurement (e.g., metric(for Celcius), imperial(for Farenheit))
            - logger_name: Name of the logger.
            - account: Account information.
            - crontimeinhhmmss: Cron time in hhmmss format.

### ./helpers/__init__.py

### ./helpers/azure_blob_client.py
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

- **__init__(
        self,
        logger_name,
        account,
        crontimeinhhmmss,
        storage_account_key=None,
        storage_account_name=None,
        storage_account_url=None,
        container_name=None,
    )**: Constructor method which captures all the required information to
        make Azure blob connection.

        Parameters:
            - logger_name: Name of the logger (string).
            - account: Account information (string).
            - crontimeinhhmmss: Cron time in hhmmss format (string).
            - storage_account_key: Azure storage account key (string).
            - storage_account_name: Azure storage account name (string).
            - storage_account_url: Azure storage account URL (string).
            - container_name: Name of the Azure container (string).

- **get_connection(self)**: Establishes connection to Azure Blob service.

        Returns:
            - BlobServiceClient: Connection to Azure Blob service.

- **create_container(self, container_name)**: Creates an Azure Blob container if it does not already exist.

        Parameters:
            - container_name: Name of the container to create (string).

        Returns:
            - container_name: The name of the created or existing container.

- **download_file(self, down_container_name, down_blob_name, down_file_path)**: Downloads a file from Azure Blob storage to the local system.

        Parameters:
            - down_container_name:
                Name of the container from which to download.
            - down_blob_name:
                Name of the blob to download (string).
            - down_file_path:
                Local file path to save the downloaded file (string).

- **upload_file(self, container_name, blob_name, file_path)**: Uploads a file from the local system to Azure Blob storage.

        Parameters:
            - container_name: Name of the container to upload to (string).
            - blob_name: Name of the blob to create (string).
            - file_path: Local file path of the file to upload (string).

- **cleanup(self, dir_path)**: Deletes the local directory and its contents.

        Parameters:
            - dir_path: Path to the directory to delete (string).

### ./helpers/create_file_helper.py
Responsible for writing given records to a CSV file at the given path.

    Parameters:
        - logger_name: Name of the logger (string).
        - file_path: Filesystem path where the final CSV/JSON file will be written (string).
        - records: Data to be written to the CSV/JSON (list or generator).
        - account: Account information (string).
        - crontimeinhhmmss: Cron time in hhmmss format (string).
        - header: The header row for the CSV (list of strings).
        - dry_run: If True, simulates writing the CSV without actually writing (boolean).

- **write_csv(
    logger_name,
    file_path,
    records,
    account,
    crontimeinhhmmss,
    header=None,
)**: Responsible for writing given records to a CSV file at the given path.

    Parameters:
        - logger_name: Name of the logger (string).
        - file_path: Filesystem path where the final CSV/JSON file will be written (string).
        - records: Data to be written to the CSV/JSON (list or generator).
        - account: Account information (string).
        - crontimeinhhmmss: Cron time in hhmmss format (string).
        - header: The header row for the CSV (list of strings).
        - dry_run: If True, simulates writing the CSV without actually writing (boolean).

- **read_csv(
    file_path,
    logger_name,
    account,
    crontimeinhhmmss,
    encoding="utf8",
)**: Reads the CSV file at the given file path and returns records.

    Parameters:
        - file_path: Filesystem path where the CSV file resides (string).
        - logger_name: Name of the logger (string).
        - account: Account information (string).
        - crontimeinhhmmss: Cron time in hhmmss format (string).
        - encoding: Encoding format for the CSV file (string, default 'utf8').

    Returns:
        - Generator yielding individual records (dict).

### ./helpers/logging_client.py
Used to check if the classs has a object already instanitated.
        If there is already a object to that class it wont create a new one
        instead it will return the one which is already generated.
        Else it will create a new object and would return the newly created one

- **__call__(cls, *args, **kwargs)**: Used to check if the classs has a object already instanitated.
        If there is already a object to that class it wont create a new one
        instead it will return the one which is already generated.
        Else it will create a new object and would return the newly created one


## Latest Update
Changes were pushed on 2024-11-14 16:16:34

## Changes in the Latest Push
