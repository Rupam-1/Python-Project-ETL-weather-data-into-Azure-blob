<h1 align="center">Welcome to dummyds</h1>
<p align="center">
  <a href="http://temp-url.com" target="_blank">
    <img alt="Documentation" src="https://img.shields.io/badge/documentation-yes-brightgreen.svg" />
  </a>
</p>

> This repository provides a versatile set of Python scripts and utilities designed to streamline the process of connecting to and fetching data from various sources like APIs, databases, and Azure storage (Blob, Table). It offers a robust and flexible data lake solution tailored for various environments.

# Features

- **API Integration**: Retrieve data from RESTful APIs, supporting both authenticated and unauthenticated endpoints with configurable request settings.
- **Multithreading & Multiprocessing**: Enhance performance for large data processing tasks using Python’s threading and multiprocessing modules, enabling concurrent execution and reducing overall processing time.
- **Modular and Extensible**: The repository is designed with modularity in mind, making it easy to extend functionalities or integrate with existing projects.
- **Error Handling & Logging**: Comprehensive error handling and logging mechanisms ensure robustness and easy debugging.

# Contents

1. [Code Layout](#code-layout)
2. [Dependencies](#dependencies)
3. [Run Steps](#run-steps)
4. [Configuration Options](#configuration-options)
5. [Run Schedules](#run-schedules)
6. [Script Execution and Logging](#script-execution-and-logging)
7. [Code Linting](#code-linting)
8. [PEP 8 Best Practices](#pep-8-best-practices)
9. [Change Process](#change-process)
10. [Code Formatting](#code-formatting)

# Code Layout

```plaintext
dummyds
├── config.ini  # Store credentials and configuration options.
├── dummy-etl.py  # The main entry point for the ETL process.
├── helpers
│   ├── azure_blob_client.py  # Helper module for Azure Blob storage interactions.
│   ├── azure_table_client.py  # Helper module for Azure Table storage interactions.
│   ├── csv_helper.py  # Helper module for creating CSV or JSON files.
│   ├── dummy_api_client.py  # Helper module for data fetching from API.
│   ├── dummy_db_client.py  # Helper module for data fetching from DataBase.
│   ├── __init__.py  # Initialize helper modules.
│   ├── logging_client.py  # Logger utilities.
│   ├── multiprocess_client.py  # Helper module for Multiprocessing.
│   └── multithreading_client.py  # Helper module for Multithreading.
├── README.md  # Project documentation.
└── requirements.txt  # Python dependencies.

1 directory, 13 files
```
# Dependencies

1. Python 3.x
2. A configuration file (`config.ini`) that includes Azure storage account credentials and other necessary settings.
3. Compatibility with Terragrunt version >= v0.17.0 (for related functionalities).
4. Config files are saved at `/opt/ihsm/configs/` location on ETL servers.

# Run Steps

```bash
# Optional: create a virtual environment
python -m venv venv

# Install required libraries
python -m pip install -r requirements.txt

# Run the main file
python dummy-etl.py
```

# Configuration options <a id="config"></a>

The `config.ini` file should include the following configuration options:

```ini
[environment]
dry_run = False  # Set to True for a dry run (no data is written to Azure). Set to False for actual data processing.
account = dev   # Set to dev or prod, to run in dev or prod environment

[dummy]
# Add any data source specific configuration here.
user=test123  # user name to login via API
password=test@123  # password for that user
url=https://example.com/test1/a  # API endpoint which you want to connect

[azure_blob_prod]
storage_account_key = your_prod_storage_account_key_here  # production Azure storage account key.
storage_account_name = your_prod_storage_account_name_here  # production Azure storage account name.
storage_account_url = your_prod_storage_account_url_here  # production Azure storage account URL.
container_name = dummy  # The name of the container in Azure Blob storage for production.

[azure_blob_dev]
storage_account_key = your_dev_storage_account_key_here  # development Azure storage account key.
storage_account_name = your_dev_storage_account_name_here  # development Azure storage account name.
storage_account_url = your_dev_storage_account_url_here  # development Azure storage account URL.
container_name = dummy-test  # The name of the container in Azure Blob storage for development.

[azure_table_prod]
storage_table_name = your_prod_table_name_here  # Storage Table name which we want to create
storage_account_key = your_prod_storage_account_key_here  # production Azure storage account key.
storage_account_name = your_prod_storage_account_name_here  # production Azure storage account name.

[azure_table_dev]
storage_table_name = your_dev_table_name_here  # Storage Table name which we want to create
storage_account_key = your_dev_storage_account_key_here  # development Azure storage account key.
storage_account_name = your_dev_storage_account_name_here  # development Azure storage account name.

[csv_config]
write_csv = True  # Set to True to enable writing data to CSV files.
csv_file_path = ./files  # Local path where CSV files will be stored.
clean_files = True  # Set to True to clean up old files before writing new ones.
upload_files = True  # Set to True to enable uploading CSV files to Azure Blob storage.


```
# Run schedules <a id="runs"></a>
This script runs once everyday.
```
# example of cronjob
5 4 * * *
```
# Script Execution and Logging
The script is scheduled to run automatically via a cron job.
- **Trigger Path**: The script is triggered from `/opt/ihsm/scheduler`
- **Log Directory**: Logs generated by the script are stored in `/opt/ihsm/logs/prod/`
Ensure that the cron job is properly configured and that the log directory has the necessary permissions for writing logs.

# Code Linting

This project uses `flake8` it is a tool for enforcing Python style guidelines (PEP 8) and checking for programming errors. Using `flake8` helps maintain a consistent code style across the project.

# Running the Linter

To run the linter, follow these steps:

```bash
# Install flake8 (included in requirements.txt)
pip install -r requirements.txt

# Run flake8 from the project root
flake8

# to ignore specific line
flake8 --ignore=E302,E501

# to exclude files or directories
flake8 --exclude=env,tests/migrations
```

# PEP 8 Best Practices

To ensure the codebase is clean, readable, and consistent, here are some key Python PEP 8 best practices that we follow:

1. **Use 4 Spaces per Indent**:
   - Use spaces instead of tabs for indentation, and ensure each level of indentation uses 4 spaces.

2. **Limit Line Length**:
   - This project uses a 100-character limit instead of the traditional 79 characters recommended by PEP 8 to better accommodate modern development practices.

3. **Blank Lines**:
   - Use two blank lines before and after top-level functions and classes.
   - Use one blank line to separate methods within a class.

4. **Imports**:
   - Group imports into three sections: standard library imports, third-party imports, and local application imports. Each group should be separated by a blank line.
   - Always import each module on a separate line (e.g., `import os`, `import sys`).

5. **Naming Conventions**:
   - Use `snake_case` for variable and function names (e.g., `my_variable`, `my_function`).
   - Use `CamelCase` for class names (e.g., `MyClass`).
   - Use all uppercase with underscores for constants (e.g., `MAX_LIMIT`).

6. **Avoid Trailing Whitespace**:
   - Ensure there is no extra whitespace at the end of lines or blank lines.

7. **Use Docstrings for All Public Modules, Classes, and Functions**:
   - Every module, class, and function should have a clear docstring describing its purpose and usage.

8. **Use Consistent and Descriptive Naming**:
   - Names should be descriptive and concise, making the code self-documenting.

9. **Use Inline Comments Sparingly**:
   - Use comments to clarify the code where necessary, but avoid redundant comments that state the obvious.

10. **Use Spaces Around Operators**:
    - Include a single space before and after binary operators (e.g., `x = y + z`), but no spaces around the equals sign for keyword arguments (e.g., `def my_function(param1=5)`).

11. **Avoid Excessive Complexity**:
    - Aim for simplicity and readability. Break down complex code into smaller, well-defined functions or methods.

12. **Use `if __name__ == "__main__":`**:
    - Use this construct to ensure that your code can be used as both a script and a module.

By adhering to these PEP 8 guidelines, we can maintain a clean, readable, and maintainable codebase.

# Change Process

Follow the steps below for making any changes to the project:

1. **Create a Work Item**:
   - Before making any changes, create a work item on the project board to track the task or feature you are working on.

2. **Create a Feature Branch**:
   - Create a new feature branch based on the work item number. The branch name should follow the format:
     ```
     git checkout -b feature_branch/<workitem_number>
     ```
   - Example:
     ```
     git checkout -b feature_branch/1234
     ```

3. **Make Your Changes**:
   - Implement the necessary changes in your feature branch. 

4. **Lint and Format the changes**:
   - Ensure that your code adheres to the project's coding standards and follows PEP 8 best practices.
   ```bash
   # Format the code with Black
   black --verbose .

   # Check for issues with Flake8
   flake8

5. **Commit Your Changes**:
   - Once the changes are complete, commit them with a meaningful commit message that references the work item:
     ```bash
     git add .
     git commit -m "Fix something (Work Item #1234)"
     ```
6. **Push the Feature Branch**:
   - Push your feature branch to the remote repository:
     ```bash
     git push -u origin feature_branch/<workitem_number>
     ```
   - Example:
     ```bash
     git push -u origin feature_branch/1234
     ```

7. **Create a Pull Request**:
   - After pushing your branch, create a pull request (PR) for the feature branch. Ensure the PR description includes relevant details about the changes and references the work item.

8. **Code Review and Approval**:
   - The pull request must be reviewed and approved by another team member before it can be merged into the main branch. Address any feedback received during the review process.

9. **Merge the Feature Branch**:
   - Once the PR is approved, merge the feature branch into the main branch. Ensure all checks and tests have passed before merging.

10. **Update Your Local Branch**:
   - After your pull request has been merged into the `main` or `master` branch, update your local branch on [ETL](#script-execution-and-logging) servers to reflect the latest changes:
     ```bash
     git checkout main
     git pull origin main
     ```
   - This ensures your local repository is synchronized with the remote repository, including the latest merged changes.

11. **Close the Work Item**:
   - After the feature branch is successfully merged and pulled locally, close the associated work item on the project board.

Following this process ensures that all changes are properly tracked, reviewed, and integrated, maintaining the integrity and quality of the codebase.

# Code Formatting

This project uses `black` for automatic code formatting to ensure consistency and adherence to PEP 8 standards. `black` formats code in a standard way, reducing the need for manual formatting and making the code review process smoother.

## Installing `black`

```bash
# install black (included in requirements.txt)
pip install black 

# Format a Single File
black path/to/your/file.py

# Format All Files in a Directory
black --verbose .

# Check Formatting Without Making Changes
black --check .
```

👤 **Fayaz Abdul**

* Email: [@fayaz.abdul](fayaz.abdul@ihsmarkit.com)