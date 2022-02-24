import argparse
import importlib
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

from testers.cpiscine.CPiscineTester import CPiscineTester
from testers.get_next_line.GetNextLineTester import GetNextLineTester
from testers.libft.LibftTester import LibftTester
from testers.printf.PrintfTester import PrintfTester
from utils.ExecutionContext import TestRunInfo, set_contex
from utils.TerminalColors import TC

logger = logging.getLogger("main")

PROJECTS = [CPiscineTester, LibftTester, GetNextLineTester, PrintfTester]


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


class Formatter(argparse.HelpFormatter):
	# use defined argument order to display usage
	def _format_usage(self, usage, actions, groups, prefix):
		if prefix is None:
			prefix = 'usage: '

		# if usage is specified, use that
		if usage is not None:
			usage = usage % dict(prog=self._prog)

		# if no optionals or positionals are available, usage is just prog
		elif usage is None and not actions:
			usage = '%(prog)s' % dict(prog=self._prog)
		elif usage is None:
			prog = '%(prog)s' % dict(prog=self._prog)
			# build full usage string
			action_usage = self._format_actions_usage(actions, groups)
			usage = ' '.join([s for s in [prog, action_usage] if s])
			usage = usage.replace("[--strict]", "[--strict]\n\t\t  ")
			usage = usage.replace("[--timeout TIMEOUT]", "[--timeout TIMEOUT]\n\t\t  ")
			# omit the long line wrapping code
		# prefix with 'usage:'
		return '%s%s\n\n' % (prefix, usage)


parser = argparse.ArgumentParser(formatter_class=Formatter)


def main():
	"""
	Executes the test framework with the given args
	"""
	pwd = os.getcwd()
	current_dir = os.path.basename(pwd)
	original_dir = os.path.abspath(os.path.join(os.path.basename(pwd), ".."))
	exercises = None

	parser = ArgumentParser("francinette",
	                        formatter_class=Formatter,
	                        description=textwrap.dedent("""
			A micro framework that allows you to test your code with more ease.

			If this command is executed inside a project or an exercise (ex##),
			then it knows automatically which tests to execute, and does. No need to pass
			arguments.
	"""))
	parser.add_argument("git_repo", nargs="?", help="If present, it uses this repository to clone the exercises from")
	parser.add_argument("exercise", nargs="*", help="If present, it executes the passed tests")
	parser.add_argument("-v", "--verbose", action="store_true", help="Activates verbose mode")
	parser.add_argument("-u", "--update", action="store_true", help="forces francinette to update")
	parser.add_argument("-s",
	                    "--strict",
	                    action="store_true",
	                    help=("It restricts the tests around memory allocation so that it reserves the correct " +
	                          "amount of memory and that checks nulls when allocating memory"))
	parser.add_argument("--part1", action="store_true", help="Execute tests of part1")
	parser.add_argument("--part2", action="store_true", help="Execute tests of part2")
	parser.add_argument("--mandatory", action="store_true", help="Executes test of the mandatory part")
	parser.add_argument("--bonus", action="store_true", help="Execute tests of bonus part")
	parser.add_argument("--timeout", action='store', default='10', help="The new timeout in seconds (by default is 10)")
	parser.add_argument("--clean-cache",
	                    action='store_true',
	                    help="Executes a script that will clean the most significant caches")
	parser.add_argument("-in",
	                    "--ignore-norm",
	                    action="store_true",
	                    help="If this flag is present then norminette will not be executed")
	parser.add_argument("-t",
	                    "--testers",
	                    nargs="*",
	                    help=("Executes the corresponding testers. If no arguments are passed, it asks the user. " +
	                          f"{TC.YELLOW}This parameter should be the last one in the command line{TC.NC}"))
	args = parser.parse_args()

	if args.update:
		file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "utils", "update.sh")
		logger.info(f"executing update with script: {file}")
		subprocess.run(file, shell=True)
		exit(0)

	if args.clean_cache:
		file = Path(os.path.realpath(__file__), "..", "utils", "clean_cache.sh").resolve()
		logger.info(f"executing cleaning of the cache with script: {file}")
		subprocess.run(str(file), shell=True)
		exit(0)

	if args.verbose:
		root = logging.getLogger()
		handler = logging.StreamHandler(sys.stdout)
		handler.setLevel(logging.DEBUG)
		formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
		handler.setFormatter(formatter)
		root.addHandler(handler)

	logger.info(f"current_dir: {current_dir}")
	if re.fullmatch(r"ex\d{2}", current_dir):
		exercises = [current_dir]
		current_dir = os.path.basename(os.path.abspath(os.path.join(current_dir, "..", "..")))
		logger.info(
		    f"Found exXX in the current dir '{exercises}'. Saving the exercise and going up a dir: '{current_dir}'")
		os.chdir("..")

	base = Path(os.path.dirname(os.path.realpath(__file__))).resolve()
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
		logger.exception(ex)


if __name__ == '__main__':
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
