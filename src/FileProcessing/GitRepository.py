import os
from ShellUtilities import Shell
import platform


def git_init(repo_path):
    try:
        shell_command_string = "git init"
        shell_command_results = Shell.execute_shell_command(shell_command_string, cwd=repo_path)
        if 'Initialized empty Git repository' not in shell_command_results.Stdout:
            raise Exception("The shell command returned an unexpected response when initializing the repo: {0}".format(shell_command_results.Stdout))
    except Exception as e:
        raise Exception("Unable to initialize git repository.") from e


def git_status(repo_path):
    try:
        shell_command_string = "git status -sb"
        shell_command_results = Shell.execute_shell_command(shell_command_string, cwd=repo_path)
        status = shell_command_results.Stdout.strip()
        if os.linesep in shell_command_results.Stdout:
            delim = os.linesep
        else:
            delim = "\n"
        status = status.split(delim)

        # Detemine the branch name
        branch = status[0].strip('##').strip()
        if platform == 'Windows':
            if branch == '## No commits yet on master':
                branch == None
        else:
            if branch == '## Initial commit on master':
                branch = None

        # Determine the state of the files in the repo
        file_states = []
        for line in status[1:]:
            repo_flag = line[0]
            index_flag = line[1]
            relative_file_path = line[3:]
            file_states.append((repo_flag, index_flag, relative_file_path))

        # Retrun a nice object
        status = {
            "branch": branch,
            "file_states": file_states
        }
        return status
    except Exception as e:
        raise Exception("Unable to get git status.") from e


def git_repo_dirty_state(repo_path):
    try:
        status = git_status(repo_path)
        return not status["file_states"]
    except Exception as ex:
        raise Exception("Unable to determine repo state.") from ex

def git_reset(repo_path, target, hard=False):
    try:
        shell_command_string = "git reset"
        if hard:
            shell_command_string += " --har"
        shell_command_string += " {0}".format(target)
        shell_command_results = Shell.execute_shell_command(shell_command_string, cwd=repo_path)
        s = ""
    except Exception as ex:
        raise Exception("Unable to reset git branch.") from ex

def get_git_branch(repo_path):
    try:
        status = git_status(repo_path)
        return status["branch"]
    except Exception as ex:
        raise Exception("Unable to determine current branch.") from ex

def repo_initialized_with_initial_checkin(repo_path):
    try:
        status = git_status(repo_path)
        if not status["branch"]:
            return False
        else:
            return True
    except Exception as ex:
        raise Exception("Unable to determine if repo was initialized.") from ex

def git_ls_files(repo_path):

    # This function will return a list of relative file paths

    try:
        shell_command_string = "git ls-files"
        shell_command_results = Shell.execute_shell_command(shell_command_string, cwd=repo_path)
        files = shell_command_results.Stdout.strip()
        if os.linesep in shell_command_results.Stdout:
            delim = os.linesep
        else:
            delim = "\n"
        files = files.Stdout.split(delim)
        return files
    except Exception as ex:
        raise Exception("Unable to get a list of files in the repository.") from ex

def file_in_repo(repo_path):

    pass

def git_add(repo_path, file_path):
    try:
        shell_command_string = "git add {0}".format(file_path)
        shell_command_results = Shell.execute_shell_command(shell_command_string, cwd=repo_path)
    except Exception as e:
        raise Exception("Unable to get git status.") from e


def dir_is_git_repo(repo_path):
    if not os.path.exists(repo_path):
        return False
    if not os.path.isdir(repo_path):
        return False
    try:
        git_status(repo_path)
    except:
        return False

    return True


def git_commit(repo_path, commit_message):
    try:
        shell_command_string = 'git commit -m "{0}"'.format(commit_message)
        shell_command_results = Shell.execute_shell_command(shell_command_string, cwd=repo_path)
        if '1 file changed' not in shell_command_results.Stdout:
            raise Exception("Unexpected results returned from git client:{0}{1}".format(os.linesep, shell_command_results.Stdout))
    except Exception as ex:
        raise Exception("Unable to commit repository '{0}'.".format(repo_path)) from ex
