import logging
import os
import re
import shutil
from pathlib import Path

from halo import Halo
from testers.BaseTester import BaseTester, run_command
from testers.libft.Alelievr import Alelievr
from testers.libft.BaseExecutor import (BONUS_FUNCTIONS, PART_1_FUNCTIONS,
                                        PART_2_FUNCTIONS)
from testers.libft.Fsoares import Fsoares
from testers.libft.Tripouille import Tripouille
from testers.libft.WarMachine import WarMachine
from utils.ExecutionContext import TestRunInfo, set_bonus
from utils.TerminalColors import TC
from utils.Utils import is_makefile_project

logger = logging.getLogger("libft")

func_regex = re.compile(r"(?:\w+\s+)+\**ft_(\w+)\s*\(.*")


class Libft(BaseTester):

	name = "libft"
	my_tester = Fsoares
	testers = [WarMachine, Tripouille, Alelievr, Fsoares]
	timeout = 2

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		super().execute_testers()

	@staticmethod
	def is_project(current_path):
		return is_makefile_project(current_path, "libft.a", Libft)

	def select_tests_to_execute(self):
		args = self.info.args
		if (args.mandatory or args.bonus):
			all_funcs = []
			if (args.mandatory):
				all_funcs.extend(PART_1_FUNCTIONS)
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
			
	def compile_source(self):
		os.chdir(os.path.join(self.temp_dir))
		makefile = Path(self.temp_dir, "Makefile")
		if not makefile.exists():
			return
		command = "make fclean all" + (" bonus" if self.has_bonus() else "")
		logger.info(f"Calling '{command}' on directory {os.getcwd()}")

		text = f"{TC.CYAN}Executing: {TC.B_WHITE}{command}{TC.NC} " + ("" if self.has_bonus() else "(no bonus)")
		with Halo(text=text) as spinner:
			run_command(command, spinner)
			spinner.succeed()
