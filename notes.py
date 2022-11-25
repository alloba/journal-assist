import sys
import os
from datetime import date
from string import Template
import subprocess

# These values are free to be accessed from anywhere in the script.
# TEMPLATE relies on the relative path between this file and the template being consistent.
# (vs a potential future case where the templates folder can be specified in some other way)
TODAY = str(date.today())  # formatted like YYYY-MM-DD
FILE_EXT = ".md"
TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/default.md')

NO_GIT = False  # skip all git operations if true.  
REMOTE_FLAG = True  # used for testing. if false, skip pushing commits to remote.
NO_EDITOR = False 

# TODO: I'd rather be able to provide default paths in the environment for the required arguments. 
#       It would make it less of a pain to set up (would just have to add them to a terminal profile)
def print_help_message():
    print("""
            journal-assist 
            Exactly 2 input arguments are accepted. The root folder of the journal (for git tracking), and the subdirectory that journal entries are stored in.
            Any additional arguments, or missing arguments, will result in this message.""")


def create_journal_file(filepath, templatepath):
    r = {"DATE": TODAY}
    template_file = open(templatepath, "r")
    template = Template(template_file.read())
    template_file.close()

    target_file = open(filepath, "w")
    target_file.write(template.substitute(r))
    target_file.close()

def trigger_pull_from_remote(root_project_directory): 
    if NO_GIT: 
        print('trigger_pull_from_remote skipped')
        return 
    subprocess.call(f'git -C {root_project_directory} fetch')
    subprocess.call(f'git -C {root_project_directory} pull')

def trigger_edit_journal_file(filepath, starting_line=0):
    if NO_EDITOR: 
        return 
    subprocess.run(f"nvim {filepath} +{starting_line}")


def trigger_track_journal_file(root_project_directory, filepath):
    if NO_GIT: 
        print('trigger_track_journal_file skipped')
        return 
    subprocess.call(f'git -C {root_project_directory} add {filepath}')


def trigger_commit(root_project_directory):
    if NO_GIT: 
        print('trigger_commit skipped')
        return 
    commit_message = f'updated journal file for {TODAY}'
    subprocess.call(f'git -C {root_project_directory} commit -m "{commit_message}"')


def trigger_push_to_remote(root_project_directory):
    if NO_GIT or not REMOTE_FLAG: 
        print('trigger_push_to_remote skipped')
        return 
    subprocess.call(f'git -C {root_project_directory} push')


if __name__ != "__main__":
    print("Not supported to run as imported resource")
    sys.exit(1)


if len(sys.argv) != 3:
    print_help_message()
    sys.exit(1)

rootDir = os.path.realpath(os.path.expanduser(sys.argv[1]))
journalDirectory = os.path.abspath(os.path.expanduser(sys.argv[2]))
journalFilePath = os.path.join(journalDirectory, TODAY + FILE_EXT)

if not os.path.exists(rootDir):
    print(f'Provided directory does not exist: {rootDir}')
    sys.exit(1)

if not os.path.exists(journalDirectory):
    print(f'Provided directory does not exist: {journalDirectory}')
    sys.exit(1)

trigger_pull_from_remote(rootDir)

dirfiles = [os.path.join(journalDirectory, f) for f in os.listdir(journalDirectory) if
            os.path.isfile(os.path.join(journalDirectory, f))]

if journalFilePath not in dirfiles:
    print(f'Journal file {journalFilePath} does not exist. Creating.')
    create_journal_file(journalFilePath, TEMPLATE)

trigger_edit_journal_file(journalFilePath)
trigger_track_journal_file(rootDir, journalFilePath)
trigger_commit(rootDir)
trigger_push_to_remote(rootDir)
print(f'Completed journal edit for {TODAY}{FILE_EXT}')
