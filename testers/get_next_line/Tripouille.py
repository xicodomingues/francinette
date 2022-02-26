import logging
import re

from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_timeout
from utils.TerminalColors import TC

logger = logging.getLogger('gnl-trip')


class Tripouille(BaseExecutor):

	name = 'gnlTester'
	folder = 'gnlTester'
	git_url = 'https://github.com/Tripouille/gnlTester'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+|LEAKS).([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):

		def handle_output(output, execute=True):
			if not execute or not output:
				return []
			lines = output.splitlines()
			if lines[1].startswith("../"):
				raise Exception(f"{TC.B_RED}Problem compiling tests.{TC.NC}")
			errors = self.check_errors(output)
			return errors

		def execute_make(command, execute=True, silent=False):
			if execute:
				return self.run_tests(command, not silent)

		timeout = f"TIMEOUT_US={get_timeout() * 1_000_000}"
		output = execute_make(f"make {timeout} m", self.exec_mandatory)
		output_bonus = execute_make(f"make {timeout} b", self.exec_bonus, True)
		print()
		errors = handle_output(output, self.exec_mandatory)

		all_errors = set(errors).union(handle_output(output_bonus, self.exec_bonus))
		self.show_test_files(all_errors, ["multiple fd"], "tests/mandatory.cpp", "tests/bonus.cpp")
		return [self.name] if all_errors else []
