import argparse
from argparse import ArgumentParser
from dataclasses import dataclass
import importlib
import logging
import os
import re
import shutil
import sys
import textwrap
from typing import List

from git import Repo

logger = logging.getLogger()
logger.setLevel(logging.WARN)


@dataclass
class TestRunInfo:
    project: str
    source_dir: str
    tests_dir: str
    temp_dir: str
    ex_to_execute: List[str]
    verbose: bool


class CT:
    WHITE = '\033[1;37m'
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    CYAN = '\033[0;36m'
    L_GREEN = '\033[1;32m'
    L_BLUE = '\033[1;36m'
    PURPLE = '\033[0;35m'
    L_PURPLE = '\033[1;35m'
    YELLOW = '\033[0;33m'
    L_YELLOW = '\033[1;33m'
    L_RED = '\033[1;31m'
    NC = '\033[0m'  # No Color


def has_file(ex_path, file):
    path = os.path.join(ex_path, file)
    logger.info(f"Testing path: {path}")
    return os.path.exists(path)


def is_library(path):
    # check for makefile
    make_path = os.path.join(path, "makefile")
    # check for name of makefile
    if not os.path.exists(make_path):
        return False
    with open(make_path, "r") as mk:
        if 'libft' in mk.read():
            return True
        else:
            return False


def is_repo(string: str):
    return string.startswith("git@")


def guess_project(current_dir):
    logger.info(f"Current dir: {current_dir}")
    ex_path = os.path.abspath("ex00")
    logger.info(f"Testing path: {ex_path}")
    if os.path.exists(ex_path):

        if has_file(ex_path, "ft_putchar.c"):
            return "c00"
        if has_file(ex_path, "ft_ft.c"):
            return "c01"
        if has_file(ex_path, "ft_strcpy.c"):
            return "c02"
        if has_file(ex_path, "ft_strcmp.c"):
            return "c03"
        if has_file(ex_path, "ft_strlen.c"):
            return "c04"
        if has_file(ex_path, "ft_iterative_factorial.c"):
            return "c05"

    if is_library(os.path.abspath('.')):
        return "libft"

    raise Exception("Francinette needs to be executed inside a project folder\n" +
                    "If you are inside a folder, please make sure that you have a valid Makefile")


def clone(repo, basedir, current_dir):
    repo_dir_temp = os.path.abspath(os.path.join(basedir, "temp", "temp_clone"))
    if os.path.exists(repo_dir_temp):
        logger.info(f"removing {repo_dir_temp} because it will be overwritten")
        shutil.rmtree(repo_dir_temp)

    logger.info(f"Cloning repo {repo} to {repo_dir_temp} and creating a copy of the repo under the username")
    cloned = Repo.clone_from(repo, repo_dir_temp)
    os.chdir(repo_dir_temp)

    project = guess_project(os.getcwd())
    master = cloned.head.reference
    author_name = str(master.commit.author.email).split('@')[0].replace(" ", "_")

    if '+' in author_name:
        author_name = author_name.split('+')[1]

    repo_copy_dir = os.path.join(current_dir, author_name + "_" + project)
    if os.path.exists(repo_copy_dir):
        shutil.rmtree(repo_copy_dir)
    cloned.clone(repo_copy_dir)
    logger.info(f"Created a copy of the repository in {repo_copy_dir}")
    return repo_copy_dir


def execute_tests(info):
    # Get the correct tester
    module_name = info.project.capitalize() + "Tester"
    module = importlib.import_module('testers.' + module_name)

    # execute the tests
    module.__getattribute__(module_name)(info)


def main():
    """
    Executes the test framework with the given args
    """
    pwd = os.getcwd()
    current_dir = os.path.basename(pwd)
    original_dir = os.path.abspath(os.path.join(os.path.basename(pwd), ".."))
    exercises = None

    parser = ArgumentParser("francinette",
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            description=textwrap.dedent("""
            A micro framework that allows you to test your code with more ease.

            If this command is executed inside a project or an exercise (ex##),
            then it knows automatically which tests to execute, and does. No need to pass
            arguments.
    """))
    parser.add_argument(
        "git_repo",
        nargs="?",
        help="If present, it uses this repository to clone the exercises from"
    )
    parser.add_argument(
        "exercise", nargs="*",
        help="If present, it executes the passed tests"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="activates verbose mode, showing more internal details of the execution"
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.INFO)

    logger.info(f"current_dir: {current_dir}")
    if re.fullmatch(r"ex\d{2}", current_dir):
        exercises = current_dir
        current_dir = os.path.basename(os.path.abspath(os.path.join(current_dir, "..", "..")))
        logger.info(
            f"Found exXX in the current dir '{exercises}'. Saving the exercise and going up a dir: '{current_dir}'")
        os.chdir("..")

    base = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    exercises = args.exercise or [exercises]
    if not is_repo(args.git_repo):
        exercises.append(args.git_repo)
        args.git_repo = None

    if exercises:
        logger.info(f"Will only execute the tests for {exercises}")

    try:
        from_git = False
        git_dir = None
        if args.git_repo:
            print(original_dir)
            git_dir = clone(args.git_repo, base, original_dir)
            exercises = None
            from_git = True

        project = guess_project(current_dir)
        mains_dir = os.path.join(base, "mains", project)

        info = TestRunInfo(project,
                           os.path.abspath(os.path.join(current_dir, "..")),
                           mains_dir,
                           os.path.join(base, "temp", project),
                           exercises,
                           args.verbose)

        logger.info(f"Test params: {info}")

        execute_tests(info)

        if from_git:
            print(f"You can see the cloned repository in {CT.WHITE}{git_dir}{CT.NC}")
    except Exception as ex:
        print(f"{CT.RED}{ex}")
        if args.verbose:
            print(ex.with_traceback())
        sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main()
