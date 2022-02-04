import logging
import re

from testers.get_next_line.BaseExecutor import BaseExecutor
from utils.TerminalColors import TC

logger = logging.getLogger('gnl-trip')

line_regex = re.compile(r"^([^:]+):(.+)$")
test_regex = re.compile(r"(\d+).([^ ]+)")
buffer_size_regex = re.compile(r"\[BUFFER_SIZE = (\d+)\]:")


class Tripouille(BaseExecutor):

	name = 'gnlTester'
	folder = 'gnlTester'
	git_url = 'https://github.com/Tripouille/gnlTester'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		output = self.run_tests("make m")
		return self.parse_output(output)

	def parse_output(self, output):

		def parse_tests(tests):
			return [(match.group(1), match.group(2)) for match in test_regex.finditer(tests)]

		def parse_line(line):
			match = line_regex.match(line)
			return (match.group(1), parse_tests(match.group(2)))

		def get_errors(result):
			return [test[0] for test in result[1] if test[1] != "OK"]

		def get_errors_for_buffer(line):
			while not buffer_size_regex.match(lines[line]):
				line += 1
			test_lines = []
			line += 1
			while line < len(lines) and not buffer_size_regex.match(lines[line]):
				test_lines.append(lines[line])
				line += 1
			results = [parse_line(line_str) for line_str in test_lines]
			errors = [error for error in results if get_errors(error)]
			return (line, errors)

		lines = output.splitlines()
		if lines[1].startswith("../"):
			raise Exception(f"{TC.B_RED}Problem compiling tests.{TC.NC}")
		line = 0
		has_errors = False
		line, errors = get_errors_for_buffer(line)
		if errors:
			has_errors = True
		line, errors = get_errors_for_buffer(line)
		if errors:
			has_errors = True
		line, errors = get_errors_for_buffer(line)
		if errors:
			has_errors = True
		if has_errors:
			print(
			    f"To see the tests open: {TC.PURPLE}/Users/fsoares-/fraaaaa/tests/get_next_line/gnlTester/tests/mandatory.cpp{TC.NC}"
			)
			return [self.name]
		return []
