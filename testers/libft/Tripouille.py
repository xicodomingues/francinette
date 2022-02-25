import logging
import os
import re
import subprocess
import sys

from halo import Halo
from testers.libft.BaseExecutor import remove_ansi_colors
from utils.ExecutionContext import get_timeout
from utils.TerminalColors import TC
from utils.Utils import is_linux

logger = logging.getLogger("tripouille")


class Tripouille():

	name = "libftTester"
	folder = "Tripouille"
	git_url = "https://github.com/Tripouille/libftTester"

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)

	def execute(self):
		self.compile_test()
		res = self.execute_tests()
		return self.show_failed_tests(res)

	def compile_test(self):

		def compile_executable(function, spinner):
			command = (f"clang++ -ldl -D TIMEOUT={get_timeout()} check.o color.o leaks.o sigsegv.o ft_{function}_test.o" +
			           f" -o ft_{function}.out -L. -lft -I. -I utils")
			res = subprocess.run(command, shell=True, capture_output=True, text=True)
			logger.info(res)
			if res.returncode != 0:
				spinner.fail()
				print(res.stderr)
				raise Exception(f"Problem creating executable for {function}")

		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()} compiling tests for Tripouille")

		text = f"{TC.CYAN}Compiling tests: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})"
		with Halo(text=text) as spinner:
			command = f"clang++ -D TIMEOUT={get_timeout()} -c -std=c++11 -I utils/ -I . utils/*.cpp "
			for file in self.to_execute:
				command += f"tests/ft_{file}_test.cpp "

			res = subprocess.run(command, shell=True, capture_output=True, text=True)
			logger.info(res)
			if res.returncode != 0:
				spinner.fail()
				print(res.stderr)
				raise Exception("Problem compiling tests")
			for function in self.to_execute:
				compile_executable(function, spinner)
			spinner.succeed()

	def execute_tests(self):

		Halo(f"{TC.CYAN}Testing:{TC.NC}").info()
		spinner = Halo(placement="right")

		def get_output(p):
			output = p.stdout
			spinner.stop()
			print(output, end="")
			return output

		def parse_line(line):
			match = re.match(r"^(\w+)\s+:.*", line)
			if (match):
				func_name = match.group(1)
				res = [(int(m.group(1)), m.group(2)) for m in re.finditer(r"(\d+)\.(\w+)", line)]
				return (func_name, res)

		def get_command(function):
			if is_linux():
				return f"valgrind -q --leak-check=full ./ft_{function}.out"
			else:
				return f"./ft_{function}.out"

		def execute_single_test(function):
			spinner.start(f"ft_{function.ljust(13)}:")
			command = get_command(function)
			logger.info(f"executing {command}")
			p = subprocess.run(command, capture_output=True, text=True, shell=True)
			logger.info(p)
			output = get_output(p)
			return parse_line(remove_ansi_colors(output))

		results = [execute_single_test(func) for func in self.to_execute]
		spinner.stop()
		logger.info(f"results: {results}")
		print()
		return results

	def show_failed_tests(self, result):

		def is_failed(test):
			return test[1] != 'OK' and test[1] != 'MOK'

		def match_failed(line, failed_tests):
			for test in failed_tests:
				if (re.match(rf"\s+/\*[ \w-]* {test[0]} [ \w-]*\*/ .*", line)):
					return test
			return False

		def print_error_lines(lines):
			for i, line, test in lines:
				print(f"{TC.RED}{test[1].ljust(3)} {TC.YELLOW}{i}: {TC.NC}{line}", end="")

		def show_failed_lines(file, failed_tests):
			with open(file) as f:
				lines = f.readlines()
				result = []
				for i, line in enumerate(lines):
					test = match_failed(line, failed_tests)
					if test:
						result.append((i, line, test))
				print_error_lines(result)

		def get_file_path(func):
			return os.path.join(self.tests_dir, "tests", f"{func}_test.cpp")

		def has_failed(res):
			failed = False
			for func, tests in res:
				for test in tests:
					if (test[1] == "MKO"):
						return "MKO"
					if (is_failed(test)):
						failed = True
			return failed

		errors = has_failed(result)
		if errors:
			if str(errors) == "MKO":
				print(f"{TC.RED}MKO{TC.NC}: test about your malloc size (this shouldn't be tested by moulinette)")
			print(f"\n{TC.B_RED}Errors in:{TC.NC}\n")

		funcs_error = []
		for func, tests in result:
			failed = [test for test in tests if is_failed(test)]
			if failed:
				test_file = get_file_path(func)
				print(f"For {TC.B_WHITE}{test_file}{TC.NC}:")
				show_failed_lines(test_file, failed)
				print()
				funcs_error.append(func)

		return funcs_error
