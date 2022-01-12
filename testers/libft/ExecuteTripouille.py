import logging
import os
import re
import subprocess
import sys
from main import CT
from testers.libft.BaseExecutor import BaseExecutor

logger = logging.getLogger()
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def remove_ansi_colors(text):
	return ansi_escape.sub('', text)


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


def parse_line(line):
	match = re.match(r"^(\w+)\s+:.*", line)
	if (match):
		func_name = match.group(1)
		res = [(int(m.group(1)), m.group(2)) for m in re.finditer(r"(\d+)\.(\w+)", line)]
		return (func_name, res)


class ExecuteTripouille(BaseExecutor):

	def __init__(self, tests_dir, temp_dir, to_execute) -> None:
		self.temp_dir = temp_dir
		self.to_execute = to_execute
		self.tests_dir = tests_dir
		self.folder = "Tripouille"
		self.git_url = "https://github.com/Tripouille/libftTester"

	def execute(self):
		self.prepare_tests()
		self.compile_test()
		res = self.execute_test()
		return self.show_failed_tests(res)

	def prepare_tests(self):
		os.chdir(os.path.join(self.temp_dir, self.folder, 'tests'))

		logger.info("Rewriting the mains to create a super main.cpp")
		for file in os.listdir("."):
			with open(file, "r") as f:
				fname = file.replace('ft_', '').replace('_test.cpp', '')
				content = f.read().replace("main(void)",
				                           f"main_{fname}(void)").replace("int iTest = 1;", 'extern int iTest;')

			logger.info(f"Saving file {file}")
			with open(file, "w") as f2:
				f2.write(content)

		logger.info("Creating the super main!")
		create_main(self.to_execute)

	def compile_test(self):
		command = (f"clang++ -g3 -ldl -std=c++11 -I utils/ -I . utils/sigsegv.cpp utils/color.cpp " +
		           f"utils/check.cpp utils/leaks.cpp tests/main.cpp -o main.out").split(" ")
		for file in self.to_execute:
			command.append(f"tests/ft_{file}_test.cpp")

		command += ["-L.", "-lft"]

		return self.compile_with(command)

	def execute_test(self):
		if sys.platform.startswith("linux"):
			execute = f"valgrind -q --leak-check=full ./main.out".split(" ")
		else:
			execute = ["./main.out"]

		print(f"\n{CT.CYAN}Executing: {CT.WHITE}{' '.join(execute)}{CT.NC}:")

		p = subprocess.run(execute, capture_output=True, text=True)
		print(p.stdout, CT.NC)

		return [parse_line(remove_ansi_colors(line)) for line in p.stdout.splitlines()]

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
