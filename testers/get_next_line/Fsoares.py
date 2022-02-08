from asyncio import subprocess
import logging
import os
from pipes import quote
import re
from typing import Set

import pexpect
from testers.get_next_line.BaseExecutor import BaseExecutor
from halo import Halo

from utils.ExecutionContext import is_strict
from utils.TerminalColors import TC
from utils.Utils import intersection, show_errors_file

logger = logging.getLogger("gnl-fsoares")

buffer_size_regex = re.compile(r"BUFFER_SIZE: (\d+)")

class Fsoares(BaseExecutor):

	name = 'fsoares'
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)


	def execute(self):

		bonus_tests = ["open, close, open", "2 file descriptors", "multiple fds", "test limit fds"]

		def execute_command(command, execute=True, silent=False):
			if not execute:
				return []
			strict = "STRICT='-D STRICT_MEM'" if is_strict() else ""
			command = f"{command} {strict}"
			output = self.run_tests(command, show_message=not silent)
			return list(self.check_errors(output))

		def show_errors(errors: Set):
			if errors:
				show_errors_file(self.temp_dir / "error_color.log", self.temp_dir / "errors.log")

			self.show_test_files(errors, bonus_tests, "tester.c", "bonus.c")

			if not is_strict() and not errors:
				print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'. " +
					f"Moulinette will not do these checks, it's only a matter of pride.")

		errors = execute_command("make mandatory", self.exec_mandatory)
		bonus_errors = set(errors).union(execute_command("make bonus", self.exec_bonus, True))
		show_errors(bonus_errors)
		return [self.name] if bonus_errors else []


