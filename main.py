import argparse
import importlib
import logging
import os
import re
import shutil
import subprocess
import textwrap
from argparse import ArgumentParser
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

from git import Repo

from utils.ExecutionContext import TestRunInfo, set_contex
from utils.TerminalColors import TC

logger = logging.getLogger("main")


def has_file(ex_path, file):
	path = os.path.join(ex_path, file)
	logger.info(f"Testing path: {path}")
	return os.path.exists(path)


def is_library(path):
	make_path = os.path.join(path, "Makefile")
	logger.info(f"Makefile path: {make_path}")
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

	raise Exception(f"Francinette needs to be executed inside a project folder\n" +
	                f"{TC.NC}If you are in a project folder, please make sure that you have a valid Makefile " +
	                f"and that you are creating the expected turn in files (for example 'libft.a')")


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
	parser.add_argument("git_repo", nargs="?", help="If present, it uses this repository to clone the exercises from")
	parser.add_argument("exercise", nargs="*", help="If present, it executes the passed tests")
	parser.add_argument("-u", "--update", action="store_true", help="forces francinette to update")
	parser.add_argument("--strict",
	                    action="store_true",
	                    help=("It restricts the tests around memory allocation so that it reserves the correct " +
	                          "amount of memory and that checks nulls when allocating memory"))
	args = parser.parse_args()

	if args.update:
		file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "utils", "update.sh")
		logger.info(f"executing update with script: {file}")
		subprocess.run(file, shell=True)
		exit(0)

	logger.info(f"current_dir: {current_dir}")
	if re.fullmatch(r"ex\d{2}", current_dir):
		exercises = [current_dir]
		current_dir = os.path.basename(os.path.abspath(os.path.join(current_dir, "..", "..")))
		logger.info(
		    f"Found exXX in the current dir '{exercises}'. Saving the exercise and going up a dir: '{current_dir}'")
		os.chdir("..")

	base = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
	exercises = args.exercise or exercises
	if args.git_repo and not is_repo(args.git_repo):
		if not exercises:
			exercises = []
		exercises.append(args.git_repo)
		logger.info(f"{args.git_repo} is not git repo")
		args.git_repo = None

	if exercises:
		logger.info(f"Will only execute the tests for {exercises}")

	try:
		from_git = False
		git_dir = None
		if args.git_repo:
			logger.info(f"paco called from: {original_dir}")
			git_dir = clone(args.git_repo, base, original_dir)
			exercises = None
			from_git = True

		project = guess_project(current_dir)
		mains_dir = os.path.join(base, "mains", project)

		info = TestRunInfo(project, os.path.abspath(os.path.join(current_dir, "..")), mains_dir,
		                   os.path.join(base, "temp", project), exercises, args.strict, False)

		logger.info(f"Test params: {info}")

		set_contex(info)
		execute_tests(info)

		if from_git:
			print(f"You can see the cloned repository in {TC.B_WHITE}{git_dir}{TC.NC}")
	except Exception as ex:
		print(f"{TC.B_RED}{ex}{TC.NC}")
		logger.exception(ex)


if __name__ == '__main__':
	logger_dir = Path(__file__, "..", "logs").resolve()
	if not logger_dir.exists():
		logger_dir.mkdir()
	handler = TimedRotatingFileHandler(logger_dir.joinpath("execution.log"), when='d', backupCount=1)
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s [%(name)s][%(levelname)s]: %(message)s')
	handler.setFormatter(formatter)
	handler.suffix += ".log"
	root = logging.getLogger()
	root.addHandler(handler)
	root.setLevel(logging.INFO)

	main()
