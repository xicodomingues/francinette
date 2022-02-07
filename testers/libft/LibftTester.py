import logging
import os
import re
import shutil
import subprocess
from collections import namedtuple
from pathlib import Path

import git
from halo import Halo
from testers.BaseTester import BaseTester
from testers.libft.Alelievr import Alelievr
from testers.libft.BaseExecutor import BONUS_FUNCTIONS, PART_1_FUNCTIONS, PART_2_FUNCTIONS
from testers.libft.Fsoares import Fsoares
from testers.libft.Tripouille import Tripouille
from testers.libft.WarMachine import WarMachine
from utils.ExecutionContext import TestRunInfo, has_bonus, is_strict, set_bonus
from utils.TerminalColors import TC

logger = logging.getLogger("libft")

func_regex = re.compile(r"\w+\s+\**ft_(\w+)\s*\(.*")


def run_command(command: str, spinner: Halo):
	to_execute = command.split(" ")
	process = subprocess.run(to_execute, capture_output=True, text=True)
	logger.info(process)

	if process.returncode != 0:
		spinner.fail()
		print(process.stderr)
		raise Exception("Problem creating the library")
	return process


class LibftTester(BaseTester):

	name = "libft"
	testers = [WarMachine, Tripouille, Alelievr, Fsoares]

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		super().execute_testers()

	@staticmethod
	def is_project(current_path):
		make_path = current_path / "Makefile"
		logger.info(f"Makefile path: {make_path.resolve()}")
		if not make_path.exists():
			return False
		with open(make_path, "r") as mk:
			if 'libft' in mk.read():
				return LibftTester
			else:
				return False

	def test_selector(self):
		result = super().test_selector()
		if is_strict() and Fsoares in result:
			return [Fsoares]
		return result

	def select_tests_to_execute(self):
		args = self.info.args
		if (args.part1 or args.part2 or args.bonus):
			all_funcs = []
			if (args.part1):
				all_funcs.extend(PART_1_FUNCTIONS)
			if (args.part2):
				all_funcs.extend(PART_2_FUNCTIONS)
			if (args.bonus):
				all_funcs.extend(BONUS_FUNCTIONS)
				set_bonus(True)
			return all_funcs

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

	def check_norminette(self):
		res = super().check_norminette()

		srcs_path = Path(self.temp_dir, "__my_srcs")
		logger.info(f"copying {self.source_dir} to {srcs_path}")
		shutil.copytree(self.source_dir, srcs_path)
		return res

	def compile_source(self):
		os.chdir(os.path.join(self.temp_dir))
		command = "make re" + (" bonus" if has_bonus() else "")
		logger.info(f"Calling '{command}' on directory {os.getcwd()}")

		text = f"{TC.CYAN}Executing: {TC.B_WHITE}{command}{TC.NC}"
		with Halo(text=text) as spinner:
			run_command(command, spinner)
			spinner.succeed()

	def prepare_tests(self, tester):
		super().prepare_tests(tester)
		temp_dir = os.path.join(self.temp_dir, tester.folder)

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

	def get_functions_present(self):
		header = os.path.join(self.temp_dir, "libft.h")
		if not os.path.exists(header):
			raise Exception(f"There is no {TC.B_RED}libft.h{TC.RED} present")
		with open(header, "r") as h:
			funcs_str = [line for line in h.readlines() if func_regex.match(line)]
			return [func_regex.match(line).group(1) for line in funcs_str]
