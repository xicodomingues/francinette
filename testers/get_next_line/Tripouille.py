import logging
import re

from testers.get_next_line.BaseExecutor import BaseExecutor
from utils.TerminalColors import TC

logger = logging.getLogger('gnl-trip')

buffer_size_regex = re.compile(r"\[BUFFER_SIZE = (\d+)\]:")


class Tripouille(BaseExecutor):

	name = 'gnlTester'
	folder = 'gnlTester'
	git_url = 'https://github.com/Tripouille/gnlTester'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+|LEAKS).([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		output = self.run_tests("make m")

		lines = output.splitlines()
		if lines[1].startswith("../"):
			raise Exception(f"{TC.B_RED}Problem compiling tests.{TC.NC}")
		return self.check_errors(output, "tests/mandatory.cpp")
