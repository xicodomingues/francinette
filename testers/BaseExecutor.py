import abc
import glob
import logging
import os
import re
import subprocess
from pathlib import Path
import sys
from typing import Set

import pexpect
from halo import Halo
from utils.ExecutionContext import get_context, get_timeout, has_bonus, is_strict
from utils.TerminalColors import TC
from utils.Utils import is_linux, remove_ansi_colors, show_errors_file

logger = logging.getLogger('base_exec')
trace_regex = re.compile(r"\d+\s+[\w.?]+\s+[\d\w]+ (\w+) \+ (\d+)")
lldb_out_regex = re.compile(r"\s+Summary: \w+.out`(\w+) \+ (\d+) at (.*)$")


class BaseExecutor:

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		self.tests_dir = tests_dir / self.folder
		self.temp_dir = temp_dir / self.folder
		self.to_execute = to_execute
		self.missing = missing
		os.chdir(self.temp_dir)
		logger.info(f"on dir {os.getcwd()}")
		args = get_context().args
		self.exec_mandatory = False
		self.exec_bonus = False
		if (not args.mandatory and not args.bonus):
			self.exec_mandatory = True
			self.exec_bonus = True
		else:
			if args.mandatory:
				self.exec_mandatory = True
			if args.bonus:
				self.exec_bonus = True
		if not has_bonus():
			self.exec_bonus = False

	@abc.abstractmethod
	def execute(self):
		pass

	def execute_command(self, command, spinner=None):
		output = ""
		inside_sanitizer = False
		add_to_file = False
		error_file = None

		def parse_out(to_output):
			nonlocal output
			nonlocal inside_sanitizer
			nonlocal error_file
			nonlocal add_to_file

			if (spinner and spinner.enabled):
				spinner.fail()
				spinner.enabled = False
				to_output = b'\r' + to_output
			decoded = to_output.decode('ascii', errors="backslashreplace")
			if inside_sanitizer or "=================================================================" in decoded:
				if not inside_sanitizer:
					error_file = open(self.temp_dir / "error_color.log", "a")
					inside_sanitizer = True
					add_to_file = True
				if add_to_file:
					error_file.write(decoded)
				if "SUMMARY: AddressSanitizer" in decoded:
					add_to_file = False
				if "==ABORTING" in decoded:
					inside_sanitizer = False
					error_file.close()
				return b''
			output += decoded
			return to_output

		logger.info(f"on dir {os.getcwd()}")
		p = pexpect.spawn(command)
		p.interact(output_filter=parse_out)
		print(TC.NC, end="")
		return remove_ansi_colors(output)

	def run_tests(self, command, show_message=True, spinner=None):
		if show_message:
			Halo(f"{TC.CYAN}Running tests: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})").info()
		return self.execute_command(command, spinner=spinner)

	def get_info_message(self, action):
		return f"{TC.CYAN}{action}: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})"

	def compile_tests(self, command):
		logger.info(f"on dir {os.getcwd()}")

		text = self.get_info_message("Compiling tests")
		with Halo(text) as spinner:
			self.execute_command(command, spinner)
			if (spinner and spinner.enabled):
				spinner.succeed()

	def check_errors(self, output):
		"""
		Checks the output for errors given a line_regex and test_regex.
		Both these regexes must have two groups.
		The returned value is an array with the first match of the line for each line that has errors

		Basically if it does not return an empty list, then it has errors
		"""

		def parse_tests(tests):
			return [(match.group(1), match.group(2)) for match in self.test_regex.finditer(tests)]

		def parse_line(line):
			match = self.line_regex.match(line)
			return (match.group(1).strip(), parse_tests(match.group(2)))

		def get_errors(result):
			temp = [test for test in result[1] if not test[1].startswith("OK")]
			if temp:
				return result[0]

		def get_errors_line(line: str):
			if self.line_regex.match(line):
				return get_errors(parse_line(line))

		return list(filter(lambda x: x is not None, [get_errors_line(line) for line in output.splitlines()]))

	def show_test_files(self, errors: Set, bonus_set, mandatory_path, bonus_path):
		bonus_err = errors.intersection(bonus_set)
		errors = errors.difference(bonus_set)
		if errors:
			test_path = self.tests_dir / mandatory_path
			print(f"To see the tests open: {TC.PURPLE}{test_path.resolve()}{TC.NC}")
			if bonus_err:
				test_path = self.tests_dir / bonus_path
				print(f"and the bonus open: {TC.PURPLE}{test_path.resolve()}{TC.NC}\n")
			else:
				print()
		if not errors and bonus_err:
			test_path = self.tests_dir / bonus_path
			print(f"To see the tests open: {TC.PURPLE}{test_path.resolve()}{TC.NC}\n")

	def get_all_makefiles_in_path(self):
		return glob.glob('../__my_srcs/**/Makefile', recursive=True)

	def add_sanitizer_to_makefiles(self):

		def rewrite_makefiles(makefile_path):
			makefile = Path(makefile_path).resolve()
			with open(makefile, 'r') as file:
				filedata = file.read()
			new_make = re.sub(r"-\bWall\b", f"-g -fsanitize=address -Wall", filedata)
			if is_linux():
				new_make = re.sub(r"-\bWall\b", f"-g -Wall", filedata)
			logger.info(f"added sanitization to makefile {makefile_path}")
			with open(makefile, 'w') as file:
				file.write(new_make)

		makefiles = self.get_all_makefiles_in_path()
		for make_path in makefiles:
			rewrite_makefiles(make_path)

	def call_make_command(self, command, execute=True, silent=False, spinner=None):
		if not execute:
			return ""
		timeout = f"TIMEOUT={get_timeout()}"
		strict = "EXEC_STRICT=1" if is_strict() else ""
		command = f"make {timeout} {strict} {command}"
		logger.info(f"executing: {command}")
		output = self.run_tests(command, show_message=not silent, spinner=spinner)
		logger.info(output)
		return output

	def execute_make_command(self, command, execute=True, silent=False, spinner=None):
		if not execute:
			return []
		output = self.call_make_command(command, execute, silent, spinner)
		return list(self.check_errors(output))

	def result(self, has_errors: bool):
		"""If has_errors return the name of the test

		Args:
			has_errors (bool): If this test has errors

		Returns:
			List: The correct output for the execute function
		"""
		return [self.name] if has_errors else []

	def show_errors_file(self, file_name, out_file="errors.log", n_lines=20):
		show_errors_file(self.temp_dir, file_name, out_file, n_lines)

	def execute_in_project_dir(self, command):
		p = subprocess.run(f"cd ..; {command}", shell=True, capture_output=True, errors="backslashreplace")
		logger.info(p)
