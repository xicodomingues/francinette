from asyncio import subprocess
import logging
import os
from pipes import quote
import re

import pexpect
from testers.get_next_line.BaseExecutor import BaseExecutor
from halo import Halo

from utils.ExecutionContext import is_strict
from utils.TerminalColors import TC

logger = logging.getLogger("gnl-fsoares")

line_regex = re.compile(r"^([^:]+):(.+)$")
test_regex = re.compile(r"(\d+).([^ ]+)")
buffer_size_regex = re.compile(r"BUFFER_SIZE: (\d+)")

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
		if not is_strict():
			print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'. " +
			      f"Moulinette will not do these checks, it's only a matter of pride.")
		return []

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
			results = [parse_line(line_str) for line_str in test_lines if line_str.strip() != ""]
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
