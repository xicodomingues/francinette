import abc
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path

import git
from halo import Halo
from utils.ExecutionContext import TestRunInfo, get_context, get_timeout, has_bonus, is_strict, set_bonus, set_timeout
from utils.TerminalColors import TC
from utils.Utils import intersection, show_banner

logger = logging.getLogger("base")

norm_func_regex = re.compile(r"^([\w\\/]+\.(?:c|h)): Error!")


def run_command(command: str, spinner: Halo):
	to_execute = command.split(" ")
	process = subprocess.run(to_execute, capture_output=True, text=True)
	logger.info(process)

	if process.returncode != 0:
		spinner.fail()
		print(process.stderr)
		raise Exception("Problem creating the library")
	return process


class BaseTester:

	name = "base"
	testers = []
	timeout = 10

	def __init__(self, info: TestRunInfo) -> None:
		self.info = info
		self.temp_dir = info.base_dir / "temp" / self.name
		self.tests_dir = info.base_dir / "tests" / self.name
		self.source_dir = info.source_dir
		if (not info.args.timeout):
			set_timeout(self.timeout)

	@staticmethod
	@abc.abstractmethod
	def is_project(current_path):
		pass

	def execute_testers(self):
		show_banner(self.name)
		testers = self.test_selector()
		with Halo(TC.CYAN + "Preparing framework" + TC.NC) as spinner:
			self.prepare_ex_files()
			spinner.succeed()

		norm_res = ""
		if not self.info.args.ignore_norm:
			norm_res = self.check_norminette()

		srcs_path = Path(self.temp_dir, "__my_srcs")
		logger.info(f"copying {self.source_dir} to {srcs_path}")
		shutil.copytree(self.source_dir, srcs_path)

		all_funcs = self.select_tests_to_execute()
		present = self.get_functions_present()
		to_execute = intersection(all_funcs, present)

		if self.info.ex_to_execute:
			to_execute = self.info.ex_to_execute

		missing = [test for test in all_funcs if test not in to_execute]
		logger.info(f"To execute: {to_execute}")
		logger.info(f"Missing: {missing}")

		self.compile_source()
		funcs_error = []
		for tester in testers:
			funcs_error.append(self.test_using(to_execute, missing, tester))
		if not self.info.ex_to_execute:
			self.show_summary(norm_res, missing, funcs_error, to_execute)

	def test_selector(self):
		selected_testers = self.info.args.testers

		if (selected_testers == None):
			if is_strict() and self.my_tester:
				return [self.my_tester]
			return self.testers
		# TODO: check valid tester
		if (selected_testers == []):
			print(f"Please select one or more of the available testers:")
			for i, tester in enumerate(self.testers):
				print(f"{TC.B_BLUE}    {i + 1}) {TC.B_WHITE}{tester.name}{TC.NC} ({tester.git_url})")
			print(f"You can pass the numbers as arguments to {TC.B_WHITE}--testers{TC.NC} to not see this prompt")
			selected_testers = [char for char in input()]

		selected_testers = [test for test in ''.join(selected_testers) if test != ' ']
		result = [self.testers[int(i) - 1] for i in selected_testers]
		if is_strict() and self.my_tester in result:
			return [self.my_tester]
		return result

	def prepare_ex_files(self):

		def check_and_delete(repo, file):
			if os.path.isfile(file) and repo.ignored(file):
				logger.info(f"removing ignored file: {file}")
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
			logger.info(f"removing {self.temp_dir / '.git'}")
			shutil.rmtree(self.temp_dir / ".git")
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

	def select_tests_to_execute(self):
		if self.has_bonus():
			set_bonus(True)
		return []

	def get_functions_present(self):
		return []

	def has_bonus(self):
		makefile = Path(self.temp_dir, "Makefile")
		if not makefile.exists():
			return
		with open(makefile, "r") as m_file:
			bonus = [line for line in m_file.readlines() if re.match(r"^\s*bonus\s*:.*", line)]
			logger.info(f"bonus investigation: {bonus}")
			return len(bonus) != 0

	def compile_source(self):
		os.chdir(os.path.join(self.temp_dir))
		makefile = Path(self.temp_dir, "Makefile")
		if not makefile.exists():
			return
		command = "make fclean " + ("bonus" if has_bonus() else "all")
		logger.info(f"Calling '{command}' on directory {os.getcwd()}")

		text = f"{TC.CYAN}Executing: {TC.B_WHITE}{command}{TC.NC} " + ("" if has_bonus() else "(no bonus)")
		with Halo(text=text) as spinner:
			run_command(command, spinner)
			spinner.succeed()

	def test_using(self, to_execute, missing, tester):
		try:
			self.prepare_tests(tester)

			tx = tester(self.tests_dir, self.temp_dir, to_execute, missing)
			return (tester.name, tx.execute())
		except Exception as ex:
			print(ex)
			if 'fraaaa' in str(get_context().base_dir):
				raise ex
			else:
				logger.exception(ex)
			return (tester.name, [tester.name])

	def prepare_tests(self, tester):
		# delete destination folder if already present
		temp_dir = os.path.join(self.temp_dir, tester.folder)
		if os.path.exists(temp_dir):
			logger.info(f"Removing already present directory {temp_dir}")
			shutil.rmtree(temp_dir)

		# copy test framework
		tester_dir = os.path.join(self.tests_dir, tester.folder)
		logger.info(f"Copying from {tester_dir} to {temp_dir}")
		shutil.copytree(tester_dir, temp_dir)

	def show_summary(self, norm: str, missing, errors, to_execute):

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
			print()
			print(f"{TC.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
			print(f"{TC.CYAN}║                 🎉🥳 {TC.B_GREEN}All tests passed! Congratulations!{TC.CYAN} 🥳🎉                 ║")
			print(f"{TC.CYAN}╚══════════════════════════════════════════════════════════════════════════════╝")
			print(TC.NC)
			logger.info("All tests ok!")
			return True

		print(f"\n{TC.B_CYAN}Summary{TC.NC}: {'' if has_bonus() else 'no bonus'}")

		logger.warn(f"norminette errors: {norm_errors}")
		if norm_errors:
			print(f"\n{TC.B_YELLOW}Norminette Errors{TC.NC}:", ', '.join(norm_errors))

		logger.warn(f"missing functions: {missing}")
		if missing:
			print(f"\n{TC.B_YELLOW}Missing functions{TC.NC}: {', '.join(missing)}")

		logger.warn(f"errors in functions: {errors}")
		if error_funcs:
			print(f"\n{TC.B_RED}Failed tests{TC.NC}: {', '.join(error_funcs)}")

		tests_ok = [test for test in to_execute if test not in errors]
		if tests_ok:
			print(f"\n{TC.B_GREEN}Passed tests{TC.NC}: {', '.join(tests_ok)}")
		exit(0)
