import abc
import logging
import os
import re
import subprocess
from pathlib import Path
from typing import Set

import pexpect
from halo import Halo
from utils.ExecutionContext import get_context, has_bonus
from utils.TerminalColors import TC
from utils.Utils import remove_ansi_colors

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
				return get_errors(parse_line(line))

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


	def add_to_error_file(self, error_file, traces):
		result = []
		i = 0
		with open(error_file) as err:
			for error in err.readlines():
				result.append(error)
				if error.startswith("Memory leak:"):
					result += traces[i]
					i += 1
		with open(error_file, 'w') as err:
			err.writelines(result)

	def add_leak_stack_trace(self, prog_name, error_file):

		def transform(line):
			match = trace_regex.match(line)
			if match:
				if match.group(1) == "0x0" or (match.group(1) == "start" and match.group(2) == "1"):
					return ''
				return f"image lookup --address {match.group(1)}+{match.group(2)}\n"
			return line

		with open(Path(self.temp_dir, "backtrace")) as bf:
			lines = bf.readlines()
		lines = [transform(line) for line in lines]
		with open(Path(self.temp_dir, "lldb_commands"), 'w') as lldbf:
			lldbf.writelines(lines)
		p = subprocess.run(f"lldb {prog_name} -s lldb_commands --batch", shell=True, capture_output=True, text=True)
		logger.info(p)
		traces = self.parse_lldb_out(p.stdout)
		self.add_to_error_file(error_file, traces)
