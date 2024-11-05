import os
import re
from datetime import datetime

def analyze_codebase():
    summary = """
This project is an ETL pipeline for weather data into Azure Blob Storage.
It includes the following components:
"""
    # Analyze Python files in the repository
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                summary += analyze_python_file(file_path)
    return summary

def analyze_python_file(file_path):
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract module-level docstring
    module_docstring = re.findall(r'"""(.*?)"""', content, re.DOTALL)
    module_summary = f"\n### {file_path}\n"
    if module_docstring:
        module_summary += f"{module_docstring[0].strip()}\n"
    
    # Extract function signatures and docstrings
    functions = re.findall(r'def (.*?)\):\n\s+"""(.*?)"""', content, re.DOTALL)
    for func, doc in functions:
        module_summary += f"\n- **{func})**: {doc.strip()}\n"
    
    return module_summary

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