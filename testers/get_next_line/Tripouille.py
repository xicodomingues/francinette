import logging
import re

from testers.get_next_line.BaseExecutor import BaseExecutor
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
			if not execute:
				return []
			lines = output.splitlines()
			if lines[1].startswith("../"):
				raise Exception(f"{TC.B_RED}Problem compiling tests.{TC.NC}")
			errors = self.check_errors(output)
			return errors

		def print_test_files(errors):
			bonus_err = "multiple fd" in errors
			errors.remove("multiple fd")
			if errors:
				test_path = self.tests_dir / "tests" / "mandatory.cpp"
				print(f"To see the tests open: {TC.PURPLE}{test_path.resolve()}{TC.NC}")
				if bonus_err:
					test_path = self.tests_dir / "tests" / "bonus.cpp"
					print(f"and the bonus open: {TC.PURPLE}{test_path.resolve()}{TC.NC}\n")
			if not errors and bonus_err:
				test_path = self.tests_dir / "tests" / "bonus.cpp"
				print(f"To see the tests open: {TC.PURPLE}{test_path.resolve()}{TC.NC}\n")

		def execute_make(command, execute=True, silent=False):
			if execute:
				return self.run_tests(command, not silent)

		output = execute_make("make m", self.exec_mandatory)
		output_bonus = execute_make("make b", self.exec_bonus, True)
		errors = handle_output(output, self.exec_mandatory)
		all_errors = set(errors).union(handle_output(output_bonus, self.exec_bonus))
		print_test_files(all_errors)
		return [self.name] if all_errors else []

