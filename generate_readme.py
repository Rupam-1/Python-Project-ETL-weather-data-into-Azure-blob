import os
from datetime import datetime

def analyze_codebase():
    # Use GitHub Copilot Labs to help generate this function
    # This function should analyze the codebase and return a summary
    summary = """
    This project is an ETL pipeline for weather data into Azure Blob Storage.
    It includes the following components:
    - Data extraction from weather APIs
    - Data transformation and cleaning
    - Data loading into Azure Blob Storage
    """
    return summary

def generate_readme():
    content = f"""
# AI Generated Project Title

## Description
{analyze_codebase()}

## Latest Update
Changes were pushed on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Changes in the Latest Push
"""
    # Get the list of changed files
    changed_files = os.popen('git diff-tree --no-commit-id --name-only -r HEAD').read().splitlines()
    for file in changed_files:
        content += f"- {file}\n"

    with open('AI_README.md', 'w') as f:
        f.write(content)

if __name__ == "__main__":
    generate_readme()