from distutils.log import error
import json
import logging
import os
import re
import shutil
from pathlib import Path

from halo import Halo
from testers.BaseTester import BaseTester, run_command
from testers.libft.Alelievr import Alelievr
from testers.libft.BaseExecutor import (BONUS_FUNCTIONS, PART_1_FUNCTIONS, PART_2_FUNCTIONS)
from testers.libft.Fsoares import Fsoares
from testers.libft.Tripouille import Tripouille
from testers.libft.WarMachine import WarMachine
from utils.ExecutionContext import TestRunInfo, set_bonus
from utils.TerminalColors import TC
from utils.Utils import is_makefile_project, run_shell, console

logger = logging.getLogger("libft")

func_regex = re.compile(r"(?:\w+\s+)+\**ft_(\w+)\s*\(.*")

FORBIDDEN_MSG = f"Problem compiling forbidden function check. Please contact me under '{TC.B_WHITE}fsoares-{TC.B_RED}' on slack"


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

	def check_forbidden(self, to_execute):
		
		def get_undefined_nm(output: str):
			return {f[1:] for f in output.splitlines() if f.startswith("_") and not f.startswith("__")}
		
		def has_forbidden(func, allowed, spinner):
			run_shell(f"gcc -L .. -l ft {func}.c -o {func}.out", FORBIDDEN_MSG, spinner)
			res = run_shell(f"nm -u {func}.out", FORBIDDEN_MSG, spinner)
			undefined = get_undefined_nm(res.stdout)
			return undefined.difference(allowed)
		
		shutil.copytree(self.tests_dir / "checks", self.temp_dir / "checks")
		os.chdir(self.temp_dir / "checks")

		library = os.path.join(self.temp_dir, "libft.a")
		if not os.path.exists(library):
			raise Exception(f"{TC.B_RED}libft.a{TC.RED} was not created. Please create it in the Makefile.")

		errors = set()
		with Halo(f"{TC.CYAN}Checking forbidden functions{TC.NC}") as spinner:
			allowed = self._allowed_funcs()
			for func in to_execute:
				forb = has_forbidden(func, allowed[func], spinner)
				if forb:
					spinner.stop()
					console.print(f"The function [cyan]{func}[/cyan] is using forbidden functions: [red]{', '.join(forb)}[/red]")
					spinner.start()
					errors.update(forb)
			spinner.text = f"{TC.CYAN}Forbidden functions{TC.NC}"
			spinner.fail() if errors else spinner.succeed()
		return errors

	def _allowed_funcs(self):
		res = {f: set() for f in PART_1_FUNCTIONS}
		res["calloc"] = {"malloc"}
		res["strdup"] = {"malloc"}

		res.update({f: {"malloc"} for f in PART_2_FUNCTIONS if not f.endswith("_fd")})
		res["split"].add("free")
		res["striteri"] = set()

		res.update({f: {"write"} for f in PART_2_FUNCTIONS if f.endswith("_fd")})

		res.update({f: set() for f in BONUS_FUNCTIONS})
		res["lstnew"] = {"malloc"}
		res["lstdelone"] = {"free"}
		res["lstclear"] = {"free"}
		res["lstmap"] = {"malloc", "free"}
		return res
