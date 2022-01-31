import abc
import logging
import os
from pydoc import text
import subprocess

import pexpect
from halo import Halo
from utils.TerminalColors import TC
from utils.Utils import remove_ansi_colors

logger = logging.getLogger('base_exec')


class BaseExecutor:

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		self.tests_dir = tests_dir / self.folder
		self.temp_dir = temp_dir / self.folder
		self.to_execute = to_execute
		self.missing = missing
		os.chdir(self.temp_dir)
		logger.info(f"on dir {os.getcwd()}")

	@abc.abstractmethod
	def execute(self):
		pass

	def show_run_tests(self, command):
		output = ""

		def parse_out(str):
			nonlocal output
			output += str.decode('ascii', errors="backslashreplace")
			return str

		logger.info(f"on dir {os.getcwd()}")
		Halo(f"{TC.CYAN}Running tests: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})").info()
		p = pexpect.spawn(command)
		p.interact(output_filter=parse_out)
		return remove_ansi_colors(output)

	def compile_tests(self, command):
		logger.info(f"on dir {os.getcwd()}")

		text = f"{TC.CYAN}Compiling tests: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})"
		with Halo(text) as spinner:
			c = subprocess.run(command.split(" "), capture_output=True, text=True)
			logger.info(c)
			if c.returncode != 0:
				spinner.fail()
				print(c.stderr)
				raise Exception("Problem compiling the tests")