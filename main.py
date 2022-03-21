import logging
import os
import re
import shutil
import subprocess
import sys
import textwrap
from argparse import ArgumentParser
from logging.handlers import RotatingFileHandler
from pathlib import Path

from git import Repo
from testers.cpiscine.CPiscine import CPiscine
from testers.get_next_line.GetNextLine import GetNextLine
from testers.libft.Libft import Libft
from testers.minitalk.Minitalk import Minitalk
from testers.pipex.Pipex import Pipex
from testers.printf.Printf import Printf
from utils.ExecutionContext import TestRunInfo, set_contex
from utils.TerminalColors import TC
from utils.update import do_update, update_paco

logger = logging.getLogger("main")

PROJECTS = [CPiscine, Libft, GetNextLine, Printf, Minitalk, Pipex]


def is_repo(string: str):
	return string.startswith("git@")


def find_all(name, path):
	result = []
	for root, _, files in os.walk(path):
		if name in files:
			result.append(os.path.join(root, name))
	return result


def has_vscode():
	if shutil.which("code") is not None:
		logger.info("vscode exists in command line")
		return True
	if Path(os.environ['HOME'], 'Downloads', "Visual Studio Code.app").exists():
		logger.info("vscode exists in the download directory")
		return True
	return False


def open_vscode(path):
	if shutil.which("code") is not None:
		subprocess.run(["code", path])
	vscode_path = Path(os.environ['HOME'], 'Downloads', "Visual Studio Code.app/Contents/Resources/app/bin/code")
	if vscode_path.exists():
		subprocess.run([vscode_path.resolve(), path])


def guess_project(current_path):
	for project in PROJECTS:
		p = project.is_project(current_path)
		if p:
			return p

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

	project = guess_project(Path("."))
	master = cloned.head.reference
	author_name = str(master.commit.author.email).split('@')[0].replace(" ", "_")

	if '+' in author_name:
		author_name = author_name.split('+')[1]

	repo_copy_dir = os.path.join(current_dir, author_name + "_" + project.name)
	if os.path.exists(repo_copy_dir):
		shutil.rmtree(repo_copy_dir)
	cloned.clone(repo_copy_dir)
	logger.info(f"Created a copy of the repository in {repo_copy_dir}")
	return repo_copy_dir


def main():
	"""
	Executes the test framework with the given args
	"""
	pwd = os.getcwd()
	current_dir = os.path.basename(pwd)
	original_dir = os.path.abspath(os.path.join(os.path.basename(pwd), ".."))
	exercises = None

	parser = ArgumentParser("francinette",
	                        description=textwrap.dedent("""
			A micro framework that allows you to test your code with more ease.

			If this command is executed inside a project or an exercise (ex##),
			then it knows automatically which tests to execute, and does. No need to pass
			arguments.
	"""))
	parser.add_argument("git_repo", nargs="?", help="If present, it uses this repository to clone the exercises from")
	parser.add_argument("exercise", nargs="*", help="If present, it executes the passed tests")
	parser.add_argument("-v", "--verbose", action="store_true", help="Activates verbose mode (basically debug)")
	parser.add_argument("-u", "--update", action="store_true", help="forces francinette to update")
	parser.add_argument("-s",
	                    "--strict",
	                    action="store_true",
	                    help=("It restricts the tests around memory allocation so that it reserves the correct " +
	                          "amount of memory and that checks nulls when allocating memory"))
	parser.add_argument("-m", "--mandatory", action="store_true", help="Executes test of the mandatory part")
	parser.add_argument("-b", "--bonus", action="store_true", help="Execute tests of bonus part")
	parser.add_argument("-tm",
	                    "--timeout",
	                    action='store',
	                    default='10',
	                    help="The new timeout in seconds (by default is 10)")
	parser.add_argument("-c",
	                    "--clean",
	                    action='store_true',
	                    help="Executes a script that will clean the caches and other temporary files")
	parser.add_argument("-in",
	                    "--ignore-norm",
	                    action="store_true",
	                    help="If this flag is present then norminette will not be executed")
	parser.add_argument("-t",
	                    "--testers",
	                    nargs="*",
	                    help=("Executes the corresponding testers. If no arguments are passed, it asks the user. " +
	                          f"{TC.YELLOW}This parameter should be the last one in the command line even after " +
	                          f"the positional parameters{TC.NC}"))
	args = parser.parse_args()

	if args.verbose:
		root = logging.getLogger()
		handler = logging.StreamHandler(sys.stdout)
		handler.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		root.addHandler(handler)

	if args.update:
		do_update()
		exit(0)

	update_paco()

	if args.clean:
		file = Path(os.path.realpath(__file__), "../bin/clean_cache.sh").resolve()
		logger.info(f"executing cleaning of the cache with script: {file}")
		subprocess.run(str(file), shell=True)
		exit(0)

	logger.info(f"current_dir: {current_dir}")
	if re.fullmatch(r"ex\d{2}", current_dir):
		exercises = [current_dir]
		current_dir = os.path.basename(os.path.abspath(os.path.join(current_dir, "..", "..")))
		logger.info(
		    f"Found exXX in the current dir '{exercises}'. Saving the exercise and going up a dir: '{current_dir}'")
		os.chdir("..")

	base = Path(__file__, "..").resolve()
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
			if has_vscode():
				open_vscode(git_dir)
			exercises = None
			from_git = True

		project = guess_project(Path('.'))
		info = TestRunInfo(Path('.').resolve(), base, exercises, args)

		logger.info(f"Test params: {info}")
		set_contex(info)
		project(info)

		if from_git:
			print(f"You can see the cloned repository in {TC.B_WHITE}{git_dir}{TC.NC}")
	except Exception as ex:
		print(f"{TC.B_RED}{ex}{TC.NC}")
		if 'fraaaa' in str(base):
			raise ex
		else:
			logger.exception(ex)


def entry_point():
	logger_dir = Path(__file__, "..", "logs").resolve()
	if not logger_dir.exists():
		logger_dir.mkdir()
	handler = RotatingFileHandler(logger_dir.joinpath("execution.log"), maxBytes=1024 * 1024, backupCount=1)
	handler.setLevel(logging.DEBUG)
	formatter = logging.Formatter('%(asctime)s [%(name)s][%(levelname)s]: %(message)s')
	handler.setFormatter(formatter)
	root = logging.getLogger()
	root.addHandler(handler)
	root.setLevel(logging.INFO)

	main()


if __name__ == '__main__':
	entry_point()