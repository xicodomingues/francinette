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

	def check_errors(self, output, test_file_path):

		def parse_tests(tests):
			return [(match.group(1), match.group(2)) for match in self.test_regex.finditer(tests)]

		def parse_line(line):
			match = self.line_regex.match(line)
			return (match.group(1), parse_tests(match.group(2)))

		def get_errors(result):
			return [test[0] for test in result[1] if not test[1].startswith("OK")]

		def has_errors_line(line: str):
			if self.line_regex.match(line):
				return len(get_errors(parse_line(line)));

		def has_errors(output: str):
			for line in output.splitlines():
				if has_errors_line(line):
					return True

		if has_errors(output):
			test_path = self.tests_dir / test_file_path
			print(f"To see the tests open: {TC.PURPLE}{test_path.resolve()}{TC.NC}")
			return [self.name]
		return []