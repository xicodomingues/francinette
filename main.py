import argparse
import importlib
import logging
import os
import re
import shutil
import sys
import textwrap
from argparse import ArgumentParser
from dataclasses import dataclass

from git import Repo


def mergefolders(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.copy(src_file, dst_dir)


def mergefolders_not_overwriting(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if not os.path.exists(dst_file):
                shutil.copy(src_file, dst_dir)


logger = logging.getLogger()
logger.setLevel(logging.WARN)



def clone(repo, project, basedir):
    repo_dir = os.path.join(basedir, "temp", project)
    if os.path.exists(repo_dir):
        logger.info(f"removing {repo_dir} because it will be overwritten")
        shutil.rmtree(repo_dir)

    logger.info(f"Cloning {project} from {repo} to {repo_dir} and creating a copy of the repo under the username")

    cloned = Repo.clone_from(repo, repo_dir)
    master = cloned.head.reference
    author_name = str(master.commit.author.email).split('@')[0].replace(" ", "_")

    if '+' in author_name:
        author_name = author_name.split('+')[1]

    repo_copy_dir = os.path.join(basedir, author_name + "_" + project)
    if os.path.exists(repo_copy_dir):
        shutil.rmtree(repo_copy_dir)
    cloned.clone(repo_copy_dir)
    logger.info(f"Created a copy of the repository in {repo_copy_dir}")
    return repo_copy_dir

def execute_tests(info):
    # Get the correct tester
    module_name = info.project.upper() + "_Tester"
    module = importlib.import_module(module_name)

    # execute the tests
    module.__getattribute__(module_name)(info)

@dataclass
class TestRunInfo():
    project: str
    source_dir: str
    tests_dir: str
    temp_dir: str
    ex_to_execute: str
    verbose: bool


class Colors:
    WHITE = '\033[1;37m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    CYAN = '\033[0;36m'
    LIGHT_GREEN = '\033[1;32m'
    LIGHT_BLUE = '\033[1;36m'
    PURPLE = '\033[0;35m'
    LIGHT_PURPLE = '\033[1;35m'
    YELLOW = '\033[0;33m'
    LIGHT_RED = '\033[1;31m'
    NC = '\033[0m'  # No Color


def main():
    """
    Executes the test framework with the given args
    """
    pwd = os.getcwd()
    current_dir = os.path.basename(pwd)
    exercise = None
    project = None
    local = None

    parser = ArgumentParser("francinette",
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            description=textwrap.dedent("""
            A micro framework that allows you to test your C code with more ease.

            If this command is executed inside a project (c##) or an exercise (ex##),
            then it knows automatically which tests to execute, and does. No need to pass
            arguments.
            If you pass the arguments, then the arguments take precedence.
    """))

    parser.add_argument(
        "-t", "--exercise", nargs="?",
        help="If present, only executes the passed test"
    )
    parser.add_argument(
        "-b", "--base", nargs="?",
        help="The base directory where the temp files are stored. It defaults to the one where this python file is"
    )
    parser.add_argument(
        "-f", "--files", nargs="?",
        help="The directory from where to get the extra files needed to run the tests (main.c, expected, etc)"
             " If defaults to the 'files' folder inside basedir"
    )
    parser.add_argument(
        "-l", "--local", nargs="?",
        help="The local directory to get your local code from. It should point to the inside of the 'C0X' folder"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="activates verbose mode, showing more internal details of the execution"
    )
    parser.add_argument(
        "project",
        nargs="?",
        help="If present, it sets the project to be executed under testing"
    )
    parser.add_argument(
        "git_repo",
        nargs="?",
        help="If present, it uses this repository to clone the exercises from"
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    logger.info(f"current_dir: {current_dir}")
    if re.fullmatch(r"ex\d{2}", current_dir):
        exercise = current_dir
        current_dir = os.path.basename(os.path.abspath(os.path.join(current_dir, "../..")))
        logger.info(f"Found exXX in the current dir '{exercise}'. Saving the exercise and going up a dir: '{current_dir}'")

    if re.fullmatch(r"[Cc]\d{2}", current_dir):
        project = current_dir
        local = os.path.abspath(".")
        logger.info(f"Was inside a C project dir'{project}'. Setting the local to the current directory: '{local}'")

    base = args.base or os.path.dirname(os.path.realpath(__file__))
    exercise = args.exercise or exercise
    if exercise:
        exercise = exercise.rjust(2, "0")
        logger.info("Will only execute the tests for ex{exercise}")

    project = args.project or project

    if not project:
        parser.print_help()
        exit(0)

    logger.info(f"local: {local}, args.local: {args.local}, base: {base}")
    source_dir = local or args.local or base
    is_git_repo = False

    if not os.path.exists(os.path.join(source_dir, "ex01")):
        source_dir = os.path.join(source_dir, project)

    if args.git_repo:
        source_dir = clone(args.git_repo, project, base)
        exercise = None
        is_git_repo = True

    info = TestRunInfo(
        project,
        source_dir,
        os.path.join(args.files or os.path.join(base, "files"), project),
        os.path.join(base, "temp", project),
        exercise,
        args.verbose)

    logger.info(f"Executing tests with info: {info}")

    execute_tests(info)

    if is_git_repo:
        print(f"You can see the cloned repository in {Colors.WHITE}{source_dir}{Colors.NC}")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main()
