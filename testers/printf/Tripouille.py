import logging
import re
import sys

from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_timeout
from utils.TerminalColors import TC
from utils.Utils import remove_ansi_colors, show_errors_file

logger = logging.getLogger('pf-trip')


class Tripouille(BaseExecutor):

	name = 'printfTester'
	folder = 'printfTester'
	git_url = 'https://github.com/Tripouille/printfTester'
	test_regex = re.compile(r"(\d+|LEAKS)\.([^ ]+)")

	category_map = {'X': 'upperx', '%': 'percent', '.': 'dot', "'": 'space', '#': 'sharp', '-': 'minus'}

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def check_errors(self, output):

		def parse_tests(tests):
			return [(match.group(1), match.group(2)) for match in self.test_regex.finditer(tests)]

		def get_errors(result):
			temp = [test[0] for test in result if not test[1].startswith("OK")]
			return temp

		result = {}
		for line in output.splitlines():
			line = remove_ansi_colors(line)
			if line.startswith("category: "):
				category = line.split(' ')[1].strip()
			if re.match(r"\d+\..*", line):
				errors = get_errors(parse_tests(line))
				if errors:
					existing = result.get(category, [])
					result[category] = existing + errors
		return result

	def execute(self):

		def handle_output(output, execute=True):
			if not execute or not output:
				return {}
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
		errors = dict(errors, **handle_output(output_bonus, self.exec_bonus))
		errors = self.show_failed_tests(errors)
		return self.result(errors)

	def show_failed_tests(self, errors):

		def match_failed(line, tests):
			for test in tests:
				if (re.match(rf"\s+TEST\({test},.*", line)):
					return test
			return False

		def print_error_lines(lines):
			for i, line in lines:
				print(f"{TC.YELLOW}{i}:{TC.NC} {line}", end="")

		def show_failed_lines(file, tests):
			with open(file) as f:
				lines = f.readlines()
				result = []
				for i, line in enumerate(lines):
					test = match_failed(line, tests)
					if test:
						result.append((i, line))
				print_error_lines(result)

		def get_file_path(category):
			category = self.category_map.get(category, category)
			return self.tests_dir / "tests" / f"{category}_test.cpp"

		orig_stdout = sys.stdout
		f = open('errors_color.log', 'w')
		sys.stdout = f

		for category, tests in errors.items():
			tests = [test for test in tests if test != 'LEAKS']
			test_file = get_file_path(category)
			if tests:
				print(f"For {TC.PURPLE}{test_file}{TC.NC}:")
				show_failed_lines(test_file, tests)
				print()
			else:
				print(f"Leaks in tests from: {TC.PURPLE}{test_file}{TC.NC}\n")

		sys.stdout = orig_stdout
		f.close()
		errors = list(errors.keys())
		if errors:
			show_errors_file(self.temp_dir, "errors_color.log", "errors.log", 20)

		return errors
