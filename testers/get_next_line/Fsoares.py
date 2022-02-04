from asyncio import subprocess
import logging
import os
from pipes import quote

import pexpect
from testers.get_next_line.BaseExecutor import BaseExecutor
from halo import Halo

from utils.ExecutionContext import is_strict
from utils.TerminalColors import TC

logger = logging.getLogger("fsoares")


class Fsoares(BaseExecutor):

	name = 'fsoares'
	folder = 'fsoares'
	git_url = 'my own tests'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		strict = "STRICT='-D STRICT_MEM'" if is_strict() else ""
		command = f"make BUFFER_SIZE=1 {strict}"
		self.run_tests(command)
		command = f"make BUFFER_SIZE=10 {strict}"
		self.run_tests(command, False)
		command = f"make BUFFER_SIZE=1000000 {strict}"
		self.run_tests(command, False)
		if not is_strict():
			print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'. " +
			      f"Moulinette will not do these checks, it's only a matter of pride.")
		return []
