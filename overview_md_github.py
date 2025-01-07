import os
import pandas as pd
from github import Github

def connect_github(markdown_table, repo_name, mid_path, github_token, github_repo):
    #git_file_path = f"{repo_name}/{mid_path}/Overview.md" if mid_path else f"{repo_name}/Overview.md"
    git_file_path = f"{mid_path}/Overview.md"
    token = Github(github_token)
    repo = token.get_repo(github_repo)

    try:
        file = repo.get_contents(git_file_path, ref="main")
        repo.update_file(
            path=git_file_path,
            message="Updating Overview.md",
            content=markdown_table,
            sha=file.sha,
            branch="main"
        )
        print(f"{git_file_path} updated successfully.")
    except Exception as e:
        repo.create_file(
            path=git_file_path,
            message="Creating Overview.md",
            content=markdown_table,
            branch="main"
        )
        print(f"{git_file_path} created successfully.")

def get_path(file_path):
    path_parts = file_path.split(os.sep)
    try:
        main_dir_index = path_parts.index('files')
        file_parts = path_parts[main_dir_index + 1:-1]
        mid_path = "/".join(file_parts) if file_parts else ""
        return mid_path
    except ValueError:
        return None

def create_overview(repo_name, github_token, github_repo):
    full_file_paths = []
    for dirpath, inner_dir_names, filenames in os.walk("files"):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            full_file_paths.append(full_path)

    for file_path in full_file_paths:
        mid_path = get_path(file_path)
        extension = os.path.splitext(file_path)[1].lower()
        df = None
        if extension == '.csv':
            df = pd.read_csv(file_path).head(10)
        elif extension == '.json':
            df = pd.read_json(file_path).head(10)
        elif extension == '.parquet':
            df = pd.read_parquet(file_path).head(10)

        if df is not None:
            markdown_table = df.to_markdown(index=False, tablefmt="pipe")
            directory = os.path.dirname(file_path)
            connect_github(markdown_table, repo_name, mid_path, github_token, github_repo)

if __name__ == "__main__":
    create_overview()
