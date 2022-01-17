from glob import glob
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
import git
from collections import namedtuple
from main import CT, TestRunInfo
from testers.CommonTester import show_banner
from testers.libft.ExecuteFsoares import ExecuteFsoares
from testers.libft.ExecuteTripouille import ExecuteTripouille
from halo import Halo

logger = logging.getLogger("libft")

Tester = namedtuple("Test", "name constructor")

AVAILABLE_TESTERS = [Tester('Tripouille', ExecuteTripouille), Tester('fsoares', ExecuteFsoares)]

FUNCTIONS_UNDER_TEST = [
    "isalpha", "isdigit", "isalnum", "isascii", "isprint", "strlen", "memset", "bzero", "memcpy", "memmove", "strlcpy",
    "strlcat", "toupper", "tolower", "strchr", "strrchr", "strncmp", "memchr", "memcmp", "strnstr", "atoi", "calloc",
    "strdup", "substr", "strjoin", "strtrim", "split", "itoa", "strmapi", "striteri", "putchar_fd", "putstr_fd",
    "putendl_fd", "putnbr_fd"
]

func_regex = re.compile(r"\w+\s+\*+ft_(\w+)\(.*")

norm_func_regex = re.compile(r"^([\w\\]+\.c): Error!")


def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3


def run_command(command: str, spinner: Halo):
	to_execute = command.split(" ")
	process = subprocess.run(to_execute, capture_output=True, text=True)
	logger.info(process)

	if process.returncode != 0:
		spinner.fail()
		print(process.stderr)
		raise Exception("Problem creating the library")
	return process


class LibftTester():

	def __init__(self, info: TestRunInfo) -> None:

		show_banner("libft")
		self.temp_dir = info.temp_dir
		self.tests_dir = info.tests_dir
		self.source_dir = info.source_dir

		self.prepare_ex_files()
		norm_res = self.check_norminette()
		self.create_library()

		present = self.get_present()
		to_execute = intersection(present, FUNCTIONS_UNDER_TEST)

		if info.ex_to_execute:
			to_execute = info.ex_to_execute

		missing = [f for f in FUNCTIONS_UNDER_TEST if f not in to_execute]
		logger.info(f"To execute: {to_execute}")
		logger.info(f"Missing: {missing}")

		everything_ok = True
		for tester in AVAILABLE_TESTERS:
			funcs_error = self.test_using(info, to_execute, missing, tester)
			if not info.ex_to_execute:
				everything_ok = self.show_summary(norm_res, present, missing, funcs_error)
			if not everything_ok:
				break

	def test_using(self, info: TestRunInfo, to_execute, missing, tester: Tester):
		self.prepare_tests(tester.name)

		if info.ex_to_execute:
			tx = tester.constructor(self.tests_dir, info.temp_dir, info.ex_to_execute, missing)
			tx.execute()
		else:
			present = self.get_present()
			to_execute = intersection(present, FUNCTIONS_UNDER_TEST)

			tx = tester.constructor(self.tests_dir, info.temp_dir, to_execute, missing)
			return tx.execute()

	def show_summary(self, norm: str, present, missing, errors):

		def get_norm_errors():

			def get_fname(line):
				return norm_func_regex.match(line).group(1)

			def is_file(line):
				return norm_func_regex.match(line)

			return [get_fname(line) for line in norm.splitlines() if is_file(line)]

		norm_errors = get_norm_errors()
		logger.warn(f"norminette errors: {norm_errors}")
		if norm_errors:
			print(f"{CT.L_RED}Norminette Errors:{CT.NC}")
			print(', '.join(norm_errors))

		logger.warn(f"missing functions: {missing}")
		if missing:
			print(f"\n{CT.L_RED}Missing functions: {CT.NC}{', '.join(missing)}")

		logger.warn(f"errors in functions: {errors}")
		if errors:
			print(f"\n{CT.L_RED}Failed tests: {CT.NC}{', '.join(errors)}")

		if not missing and not norm_errors and not errors:
			print(f"🎉🥳 {CT.L_GREEN}All tests passed! Congratulations!{CT.NC} 🥳🎉")
			logger.info("All tests ok!")
			return True
		return False

	def prepare_ex_files(self):

		def check_and_delete(repo, file):
			if os.path.isfile(file) and repo.ignored(file):
				logger.info("removing ignored file: {file}")
				os.remove(file)

		if os.path.exists(self.temp_dir):
			logger.info(f"Removing already present directory {self.temp_dir}")
			shutil.rmtree(self.temp_dir)

		logger.info(f"copying {self.source_dir} to {self.temp_dir}")
		shutil.copytree(self.source_dir, self.temp_dir)

		try:
			repo = git.Repo(self.temp_dir)
			for path in Path(self.temp_dir).glob("*"):
				if not path.match(".git") and path.is_dir():
					for file in path.rglob("*"):
						check_and_delete(repo, file)
				if path.is_file():
					check_and_delete(repo, path)
		except Exception as ex:
			logger.exception(ex)


	def check_norminette(self):
		os.chdir(os.path.join(self.temp_dir))
		logger.info(f"On directory {os.getcwd()}")
		norm_exec = ["norminette", "-R", "CheckForbiddenSourceHeader"]

		text = f"{CT.CYAN}Executing: {CT.WHITE}{' '.join(norm_exec)}{CT.NC}"
		with Halo(text=text) as spinner:
			result = subprocess.run(norm_exec, capture_output=True, text=True)
			logger.info(result)
			if result.returncode != 0:
				spinner.fail()
				print(f"{CT.YELLOW}{result.stdout}{CT.NC}")
			else:
				spinner.succeed()

			return result.stdout

	def create_library(self):
		logger.info(f"Calling 'make re' on directory {os.getcwd()}")

		text = f"{CT.CYAN}Executing: {CT.WHITE}make re{CT.NC}"
		with Halo(text=text) as spinner:
			run_command("make re", spinner)
			spinner.succeed()

	def prepare_tests(self, testname):
		# delete destination folder if already present
		temp_dir = os.path.join(self.temp_dir, testname)
		if os.path.exists(temp_dir):
			logger.info(f"Removing already present directory {temp_dir}")
			shutil.rmtree(temp_dir)

		# copy test framework
		tester_dir = os.path.join(self.tests_dir, testname)
		logger.info(f"Copying from {tester_dir} to {temp_dir}")
		shutil.copytree(tester_dir, temp_dir)

		# copy compiled library
		library = os.path.join(self.temp_dir, "libft.a")
		if not os.path.exists(library):
			raise Exception(f"{CT.L_RED}libft.a{CT.RED} was not created. Please create it in the Makefile.")
		logger.info(f"Copying libft.a from {library} to {temp_dir}")
		shutil.copy(library, temp_dir)

		# copy header
		header = os.path.join(self.temp_dir, "libft.h")
		logger.info(f"Copying libft.h from {header} to {temp_dir}")
		shutil.copy(header, temp_dir)

		return True

	def get_present(self):
		header = os.path.join(self.temp_dir, "libft.h")
		if not os.path.exists(header):
			raise Exception(f"There is no {CT.L_RED}libft.h{CT.RED} present")
		with open(header, "r") as h:
			funcs_str = [line for line in h.readlines() if func_regex.match(line)]
			return [func_regex.match(line).group(1) for line in funcs_str]
