import sys
import os
from datetime import date
from string import Template
import subprocess

if __name__ != "__main__":
    print("Not supported to run as imported resource")
    sys.exit(1)

TODAY = str(date.today())
FILE_EXT = ".md"
TEMPLATE = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'templates/default.md')


def printHelp():
    print("""
            journal-assist 
            Exactly 2 input arguments are accepted. The root folder of the journal (for git tracking), and the subdirectory that journal entries are stored in.
            Any additional arguments, or missing arguments, will result in this message.""")


def createJournalFile(filepath, templatepath):
    r = {"DATE":TODAY}
    templateFile = open(templatepath, "r")
    template = Template(templateFile.read())
    templateFile.close()

    targetFile = open(filepath, "w")
    targetFile.write(template.substitute(r))
    targetFile.close()

def triggerEditJournalFile(filepath): 
    subprocess.run(f"nvim {filepath}")    

def triggerTrackJournalFile(rootProjectDirectory, filepath):
    subprocess.call(f'git -C {rootProjectDirectory} add {rootProjectDirectory}')

def triggerCommitJournalFile(rootProjectDirectory, filepath): 
    commitMessage = f'updated journal file for {TODAY}'
    subprocess.call(f'git -C {rootProjectDirectory} commit -m {"commitMessage"}')
def triggerPushToRemote(rootProjectDirectory): 
    print('would push remote here')


if len(sys.argv) != 3:
    printHelp()
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

dirfiles = [os.path.join(journalDirectory,f) for f in os.listdir(journalDirectory) if os.path.isfile(os.path.join(journalDirectory,f))]
if journalFilePath not in dirfiles:
    print(f'Journal file {journalFilePath} does not exist. Creating.')
    createJournalFile(journalFilePath, TEMPLATE)

triggerEditJournalFile(journalFilePath)
triggerTrackJournalFile(rootDir, journalFilePath)
triggerCommitJournalFile(rootDir, journalFilePath)
triggerPushToRemote(rootDir)

