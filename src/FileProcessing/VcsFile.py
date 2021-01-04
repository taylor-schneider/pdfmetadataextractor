from FileProcessing import GitRepository
import os
import shutil

def get_file_repo_path(file_identifier, directories):
    return os.path.join(directories["wip"], file_identifier)

def cleanup_old_wip(file_identifier, directories):
    try:
        repository_directory = get_file_repo_path(file_identifier, directories)
        if os.path.exists(repository_directory):
            shutil.rmtree(repository_directory)
    except Exception as ex:
        raise Exception("Unable to cleanup old wip for file '{0}'.".format(file_identifier)) from ex

def create_repo_and_add_file(abs_file_path, file_identifier, directories):

    # This function assumes the repository/directory does not already exist

    try:
        # Initialize the repo
        repository_directory = get_file_repo_path(file_identifier, directories)
        os.makedirs(repository_directory)
        GitRepository.git_init(repository_directory)

        # Add the file to the index
        repo_file_name = "{0}.pdf".format(file_identifier)
        abs_repo_file_path = os.path.join(repository_directory, repo_file_name)
        shutil.copy(abs_file_path, abs_repo_file_path)
        GitRepository.git_add(repository_directory, repo_file_name)

        # Commit the changes
        GitRepository.git_commit(repository_directory, "Initial checkin")

    except Exception as ex:
        raise Exception("Unable to create repository") from ex

