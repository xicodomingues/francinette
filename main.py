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

logger = logging.getLogger()
logger.setLevel(logging.WARN)

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
    LIGHT_YELLOW = '\033[1;33m'
    LIGHT_RED = '\033[1;31m'
    NC = '\033[0m'  # No Color


def guess_project(current_dir):
    logger.info(f"Current dir: {current_dir}")
    ex_path = os.path.abspath("ex00")
    logger.info(f"Testing path: {ex_path}")
    if (os.path.exists(ex_path)):

        path = os.path.join(ex_path, "ft_putchar.c")
        logger.info(f"Testing path: {path}")
        if (os.path.exists(path)):
            return "C00";

        path = os.path.join(ex_path, "ft_ft.c")
        logger.info(f"Testing path: {path}")
        if (os.path.exists(path)):
            return "C01"

        path = os.path.join(ex_path, "ft_strcpy.c")
        logger.info(f"Testing path: {path}")
        if (os.path.exists(path)):
            return "C02";

        path = os.path.join(ex_path, "ft_strcmp.c")
        logger.info(f"Testing path: {path}")
        if (os.path.exists(path)):
            return "C03";

    raise Exception("Francinette needs to be executed inside a project folder")


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
    module_name = info.project.upper() + "_Tester"
    module = importlib.import_module(module_name)

    # execute the tests
    module.__getattribute__(module_name)(info)


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
    """))
    parser.add_argument(
        "-m", "--mains", nargs="?",
        help="Sets this directory as the directory where the main.c and expected files are present. "
            "If this parameter is present, the default main.c files will be ignored"
    )
    parser.add_argument(
        "-t", "-e", "--exercise", nargs="?",
        help="If present, only executes the passed test"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        help="activates verbose mode, showing more internal details of the execution"
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
        current_dir = os.path.basename(os.path.abspath(os.path.join(current_dir, "..", "..")))
        logger.info(f"Found exXX in the current dir '{exercise}'. Saving the exercise and going up a dir: '{current_dir}'")
        os.chdir("..")

    base = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    exercise = args.exercise or exercise
    if exercise:
        exercise = "ex" + exercise.rjust(2, "0")[-2:]
        logger.info(f"Will only execute the tests for {exercise}")

    try:
        from_git = False
        if args.git_repo:
            source_dir = clone(args.git_repo, base, current_dir)
            exercise = None
            from_git = True

        project = guess_project(current_dir);

        mains_dir = os.path.join(base, "mains", project)
        if args.mains:
            mains_dir = os.path.join(args.mains, project)

        info = TestRunInfo(project,
                os.path.abspath(os.path.join(current_dir, "..")),
                mains_dir,
                os.path.join(base, "temp", project),
                exercise,
                args.verbose)

        logger.info(f"Test params: {info}")

        execute_tests(info)

        if from_git:
            print(f"You can see the cloned repository in {Colors.WHITE}{source_dir}{Colors.NC}")
    except Exception as ex:
        print(f"{Colors.RED}{ex}")
        sys.exit()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    main()
