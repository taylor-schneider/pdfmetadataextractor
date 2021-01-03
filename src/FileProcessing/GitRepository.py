import os


def create_repository_for_file(abs_file_path, directories):
    file_name = os.path.basename(abs_file_path)
    wip_repo_path = os.path.join(directories["wip"], "")
