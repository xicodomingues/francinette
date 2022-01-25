import logging
import os
import re
import shutil
import subprocess
from collections import namedtuple
from pathlib import Path

import git
from halo import Halo
from testers.libft.ExecuteAlelievr import ExecuteAlelievr
from utils.ExecutionContext import BONUS_FUNCTIONS, PART_1_FUNCTIONS, PART_2_FUNCTIONS, TestRunInfo, has_bonus, intersection, is_strict, set_bonus

from testers.CommonTester import show_banner
from testers.libft.ExecuteFsoares import ExecuteFsoares
from testers.libft.ExecuteTripouille import ExecuteTripouille
from testers.libft.ExecuteWarMachine import ExecuteWarMachine
from utils.TerminalColors import TC

logger = logging.getLogger("libft")

Tester = namedtuple("Test", "name constructor")

AVAILABLE_TESTERS = [
    Tester('war-machine', ExecuteWarMachine),
    Tester('Tripouille', ExecuteTripouille),
	Tester('alelievr', ExecuteAlelievr),
    Tester('fsoares', ExecuteFsoares)
]

func_regex = re.compile(r"\w+\s+\**ft_(\w+)\(.*")

norm_func_regex = re.compile(r"^([\w\\]+\.c): Error!")


def run_command(command: str, spinner: Halo):
	to_execute = command.split(" ")
	process = subprocess.run(to_execute, capture_output=True, text=True)
	logger.info(process)

	if process.returncode != 0:
		spinner.fail()
		print(process.stderr)
		raise Exception("Problem creating the library")
	return process


def test_selector(info: TestRunInfo):
	testers = info.args.testers
	if (testers == None):
		return AVAILABLE_TESTERS
	if (testers == []):
		print(f"Please select one or more of the available testers:")
		print(f"{TC.B_BLUE}    1) {TC.B_WHITE}war-machine{TC.NC} (https://github.com/y3ll0w42/libft-war-machine)")
		print(f"{TC.B_BLUE}    2) {TC.B_WHITE}Tripouille{TC.NC} (https://github.com/Tripouille/libftTester)")
		print(f"{TC.B_BLUE}    3) {TC.B_WHITE}alelievr{TC.NC} (https://github.com/alelievr/libft-unit-test)")
		print(f"{TC.B_BLUE}    4) {TC.B_WHITE}fsoares{TC.NC} (my own tests)")
		print(f"You can pass the numbers as arguments to {TC.B_WHITE}--testers{TC.NC} to not see this prompt")
		testers = [char for char in input()]
	testers = [test for test in ''.join(testers) if test != ' ']
	return [AVAILABLE_TESTERS[int(i) - 1] for i in testers]

class LibftTester():

	def __init__(self, info: TestRunInfo) -> None:

		show_banner("libft")

		testers = test_selector(info)

		self.temp_dir = info.temp_dir
		self.tests_dir = info.tests_dir
		self.source_dir = info.source_dir

		self.prepare_ex_files()
		norm_res = self.check_norminette()

		srcs_path = Path(self.temp_dir, "__my_srcs")
		logger.info(f"copying {self.source_dir} to {srcs_path}")
		shutil.copytree(self.source_dir, srcs_path)

		all_funcs = self.select_functions_to_execute(info)
		self.create_library()
		present = self.get_present();
		to_execute = intersection(all_funcs, present)

		if info.ex_to_execute:
			to_execute = info.ex_to_execute

		missing = [f for f in all_funcs if f not in to_execute]
		logger.info(f"To execute: {to_execute}")
		logger.info(f"Missing: {missing}")

		funcs_error = []
		for tester in testers:
			funcs_error.append(self.test_using(info, to_execute, missing, tester))
		if not info.ex_to_execute:
			self.show_summary(norm_res, present, missing, funcs_error, to_execute)

	def select_functions_to_execute(self, info: TestRunInfo):
		args = info.args;
		if (args.part1 or args.part2 or args.bonus):
			all_funcs = []
			if (args.part1):
				all_funcs.extend(PART_1_FUNCTIONS)
			if (args.part2):
				all_funcs.extend(PART_2_FUNCTIONS)
			if (args.bonus):
				all_funcs.extend(BONUS_FUNCTIONS)
				set_bonus(True)
			return all_funcs;

		all_funcs = PART_1_FUNCTIONS + PART_2_FUNCTIONS
		if self.has_bonus():
			all_funcs = all_funcs + BONUS_FUNCTIONS
			set_bonus(True)
		return all_funcs

	def has_bonus(self):
		makefile = Path(self.temp_dir, "Makefile")
		with open(makefile, "r") as m_file:
			bonus = [line for line in m_file.readlines() if re.match(r"^\s*bonus\s*:.*", line)]
			logger.info(f"bonus investigation: {bonus}")
			return len(bonus) != 0

	def test_using(self, info: TestRunInfo, to_execute, missing, tester: Tester):
		try:
			self.prepare_tests(tester.name)

			tx = tester.constructor(self.tests_dir, info.temp_dir, to_execute, missing)
			return (tester.name, tx.execute())
		except Exception as ex:
			print(ex)
			logger.exception(ex)
			return (tester.name, [])

	def show_summary(self, norm: str, present, missing, errors, to_execute):

		def get_norm_errors():

			def get_fname(line):
				return norm_func_regex.match(line).group(1)

			def is_file(line):
				return norm_func_regex.match(line)

			return [get_fname(line) for line in norm.splitlines() if is_file(line)]

		norm_errors = get_norm_errors()
		error_funcs = set()
		for results in errors:
			error_funcs = error_funcs.union(results[1])

		has_errors = missing or norm_errors or error_funcs
		if (not has_errors):
			print(f"\n🎉🥳 {TC.B_GREEN}All tests passed! Congratulations!{TC.NC} 🥳🎉")
			logger.info("All tests ok!")
			if not is_strict():
				print(f"\nWant some more thorough tests? run {TC.B_PURPLE}francinette{TC.NC}" +
					  f" with {TC.B_WHITE}--strict{TC.NC}")
			return True

		print(f"\n{TC.B_CYAN}Summary{TC.NC}:\n")

		logger.warn(f"norminette errors: {norm_errors}")
		if norm_errors:
			print(f"{TC.B_YELLOW}Norminette Errors:{TC.NC}", ', '.join(norm_errors))

		logger.warn(f"missing functions: {missing}")
		if missing:
			print(f"\n{TC.B_RED}Missing functions: {TC.NC}{', '.join(missing)}")

		logger.warn(f"errors in functions: {errors}")
		if error_funcs:
			print(f"\n{TC.B_RED}Failed tests: {TC.NC}{', '.join(error_funcs)}")

		tests_ok = [test for test in to_execute if test not in errors]
		if error_funcs:
			print(f"\n{TC.B_GREEN}Passed tests: {TC.NC}{', '.join(tests_ok)}")
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
			os.removedirs(".git")
		except Exception as ex:
			logger.exception(ex)

	def check_norminette(self):
		os.chdir(os.path.join(self.temp_dir))
		logger.info(f"On directory {os.getcwd()}")
		norm_exec = ["norminette"]

		text = f"{TC.CYAN}Executing: {TC.B_WHITE}{' '.join(norm_exec)}{TC.NC}"
		with Halo(text=text) as spinner:
			result = subprocess.run(norm_exec, capture_output=True, text=True)
			logger.info(result)
			if result.returncode != 0:
				spinner.fail()
				print(f"{TC.YELLOW}{result.stdout}{TC.NC}")
			else:
				spinner.succeed()

			return result.stdout

	def create_library(self):
		os.chdir(os.path.join(self.temp_dir))
		command = "make re" + (" bonus" if has_bonus() else "")
		logger.info(f"Calling '{command}' on directory {os.getcwd()}")

		text = f"{TC.CYAN}Executing: {TC.B_WHITE}{command}{TC.NC}"
		with Halo(text=text) as spinner:
			run_command(command, spinner)
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
			raise Exception(f"{TC.B_RED}libft.a{TC.RED} was not created. Please create it in the Makefile.")
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
			raise Exception(f"There is no {TC.B_RED}libft.h{TC.RED} present")
		with open(header, "r") as h:
			funcs_str = [line for line in h.readlines() if func_regex.match(line)]
			return [func_regex.match(line).group(1) for line in funcs_str]
