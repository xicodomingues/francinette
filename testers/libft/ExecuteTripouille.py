import logging
import os
import re
import subprocess
import sys
from main import CT
from testers.libft.BaseExecutor import remove_ansi_colors
from halo import Halo

logger = logging.getLogger()


def create_main(funcs):
	with open('main.cpp', 'w') as f:
		for func in funcs:
			f.write(f"int main_{func}(void);\n")

		f.write("\nint iTest = 1;\n")
		f.write("int main(void) {\n")
		for func in funcs:
			f.write(f"    iTest = 1;\n")
			f.write(f"    main_{func}();\n")
		f.write("}\n")


class ExecuteTripouille():

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		self.folder = "Tripouille"
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)
		self.git_url = "https://github.com/Tripouille/libftTester"

	def execute(self):
		self.compile_test()
		res = self.execute_test()
		return self.show_failed_tests(res)

	def compile_test(self):
		def compile_executable(function, spinner):
			command = (f"clang++ -ldl check.o color.o leaks.o sigsegv.o ft_{function}_test.o" +
					f" -o ft_{function}.out -L. -lft -I. -I utils");
			res = subprocess.run(command, shell=True, capture_output=True, text=True)
			if res.returncode != 0:
				spinner.fail()
				print(res.stdout)
				raise Exception(f"Problem creating executable for {function}");

		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()}")

		text = f"{CT.CYAN}Compiling tests: {CT.WHITE}{self.folder}{CT.NC} ({self.git_url})"
		with Halo(text=text) as spinner:
			command = f"clang++ -c -std=c++11 -I utils/ -I . utils/*.cpp "
			for file in self.to_execute:
				command += f"tests/ft_{file}_test.cpp "

			res = subprocess.run(command, shell=True, capture_output=True, text=True)
			if res.returncode != 0:
				spinner.fail()
				print(res.stderr)
				raise Exception("Problem compiling tests");
			for function in self.to_execute:
				compile_executable(function, spinner)
			spinner.succeed()

	def execute_test(self):

		def parse_line(line):
			match = re.match(r"^(\w+)\s+:.*", line)
			if (match):
				func_name = match.group(1)
				res = [(int(m.group(1)), m.group(2)) for m in re.finditer(r"(\d+)\.(\w+)", line)]
				return (func_name, res)

		def execute_single_test(function):
			if sys.platform.startswith("linux"):
				execute = f"valgrind -q --leak-check=full ./ft_{function}.out".split(" ")
			else:
				execute = [f"./ft_{function}.out"]
			logger.info(f"Executing: {' '.join(execute)}")
			p = subprocess.run(execute, capture_output=True, text=True)
			print(p.stdout + CT.NC, end="")
			return parse_line(remove_ansi_colors(p.stdout))

		print(f"{CT.CYAN}Executing Tests:{CT.NC}")
		return [execute_single_test(func) for func in self.to_execute]

	def show_failed_tests(self, result):

		def is_failed(test):
			return test[1] != 'OK' and test[1] != 'MOK'

		def match_failed(line, failed_tests):
			for test in failed_tests:
				if (re.match(rf"\s+/\* {test[0]} \*/ .*", line)):
					return test
			return False

		def print_error_lines(lines):
			for i, line, test in lines:
				print(f"{CT.RED}{test[1].ljust(3)} {CT.YELLOW}{i}: {CT.NC}{line}", end="")

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
				print(f"{CT.RED}MKO{CT.NC}: test about your malloc " +
				      "size (this shouldn't be tested by moulinette)")
			print(f"{CT.L_RED}Errors in:{CT.NC}")
			print()

		funcs_error = []
		for func, tests in result:
			failed = [test for test in tests if is_failed(test)]
			if failed:
				test_file = get_file_path(func)
				print(f"For {CT.WHITE}{test_file}{CT.NC}:")
				show_failed_lines(test_file, failed)
				print()
				funcs_error.append(func)

		return funcs_error
