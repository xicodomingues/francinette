import abc
from fileinput import close
import logging
import os
from typing import Set

import pexpect
from halo import Halo
from utils.ExecutionContext import get_context, has_bonus
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
		args = get_context().args;
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
		print(TC.NC)
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

	def check_errors(self, output):

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
				return get_errors(parse_line(line));

		return filter(lambda x: x is not None, [get_errors_line(line) for line in output.splitlines()])

	def show_test_files(self, errors: Set, bonus_set, mandatory_path, bonus_path):
			bonus_err = errors.intersection(bonus_set)
			errors = errors.difference(bonus_set)
			if errors:
				test_path = self.tests_dir / mandatory_path
				print(f"To see the tests open: {TC.PURPLE}{test_path.resolve()}{TC.NC}")
				if bonus_err:
					test_path = self.tests_dir / bonus_path
					print(f"and the bonus open: {TC.PURPLE}{test_path.resolve()}{TC.NC}\n")
			if not errors and bonus_err:
				test_path = self.tests_dir / bonus_path
				print(f"To see the tests open: {TC.PURPLE}{test_path.resolve()}{TC.NC}\n")