import abc
import logging
import os

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

	def execute_command(self, command, spinner=None):
		output = ""

		def parse_out(str):
			nonlocal output
			if (spinner and spinner.enabled):
				spinner.fail()
				spinner.enabled = False
				str = b'\r' + str
			output += str.decode('ascii', errors="backslashreplace")
			return str

		logger.info(f"on dir {os.getcwd()}")
		p = pexpect.spawn(command)
		p.interact(output_filter=parse_out)
		print()
		return remove_ansi_colors(output)

	def run_tests(self, command, show_message=True):
		if show_message:
			Halo(f"{TC.CYAN}Running tests: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})").info()
		return self.execute_command(command)

	def compile_tests(self, command):
		logger.info(f"on dir {os.getcwd()}")

		text = f"{TC.CYAN}Compiling tests: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})"
		with Halo(text) as spinner:
			self.execute_command(command, spinner)
			if (spinner and spinner.enabled):
				spinner.succeed()
