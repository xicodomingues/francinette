import logging
import os
from pathlib import Path
from pipes import quote
import re
import subprocess
from typing import Set

from halo import Halo
from pexpect import run
from testers.libft.BaseExecutor import remove_ansi_colors
from utils.ExecutionContext import has_bonus, is_strict
from utils.TerminalColors import TC
from utils.Utils import open_ascii

logger = logging.getLogger("fsoares")

test_regex = re.compile(r"ft_(\w+)\s*: (.*)")


class Fsoares():

	name = "fsoares"
	folder = name
	git_url = "my own tests"

	def __init__(self, tests_dir, temp_dir, to_execute: Set[str], missing) -> None:
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)
		self.git_url = None

	def execute(self):
		self.compile_test()
		result = self.execute_tests()
		logger.info(f"result: {result}")
		print()
		return self.show_failed(result)

	def compile_test(self):
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()}")

		text = f"{TC.CYAN}Compiling tests: {TC.B_WHITE}{self.folder}{TC.NC} (my own)"
		with Halo(text=text) as spinner:
			for func in self.to_execute:
				strict = " -DSTRICT_MEM" if is_strict() else ""
				bonus = " list_utils.c" if has_bonus() else ""
				command = (f"gcc{strict} -Wall -Wextra -Werror utils.c{bonus} " +
				           f"test_{func}.c malloc_mock.c -L. -lft -o test_{func}.out -ldl")
				logger.info(f"executing {command}")
				res = subprocess.run(command, shell=True, capture_output=True, text=True)
				logger.info(res)
				if res.returncode != 0:
					spinner.fail()
					print(res.stderr)
					raise Exception("Problem compiling the tests")
			spinner.succeed()

	def execute_tests(self):
		Halo(f"{TC.CYAN}Testing:{TC.NC}").info()
		spinner = Halo(placement="right")

		def parse_output(output: str, func):
			lines = output.splitlines()
			if not lines:
				return (func, "Execution Problem", ["Execution Problem"])
			if lines[-1] == "":
				lines = lines[:-1]
			match = test_regex.match(lines[-1])
			return (match.group(1), match.group(2), lines)

		def get_output(func, output):
			spinner.stop()
			print(output, end="")
			return output

		def execute_test(func):
			spinner.start(f"ft_{func.ljust(13)}:")
			out, code = run("sh -c " + quote(f"./test_{func}.out"), withexitstatus=1)
			output = out.decode('ascii', errors="backslashreplace")
			logger.info(output)
			output = get_output(func, output)
			return parse_output(remove_ansi_colors(output), func)

		result = [execute_test(func) for func in self.to_execute]
		logger.info(f"tests result: {result}")
		spinner.stop()
		return result

	def show_failed(self, output):

		def is_error(result):
			return result != "OK" and result != "No test yet"

		def build_error_file(errors):
			with open("errors_color.log", "w") as error_log:
				for func in errors:
					path = Path(self.tests_dir, f"test_{func}.c").resolve()
					error_log.write(f"For {TC.CYAN}ft_{func}{TC.NC}, in {TC.B_WHITE}{path}{TC.NC}:\n\n")
					with open_ascii(f"errors_{func}.log", "r") as f_error:
						error_log.write(f_error.read())

		def show_errors_file():
			file = Path(self.temp_dir, "errors_color.log")
			with open_ascii(file) as f:
				lines = f.readlines()
			print()
			[print(line, end='') for line in lines[:50]]
			if len(lines) > 50:
				dest = Path(self.temp_dir, 'errors.log').resolve()
				with open_ascii(file, "r") as orig, open(dest, "w") as log:
					log.write(remove_ansi_colors(orig.read()))
				print(f"...\n\nFile too large. To see full report open: {TC.PURPLE}{dest}{TC.NC}\n")
			print()

		errors = []
		for func, res, lines in output:
			if (is_error(res)):
				errors.append(func)
		logger.warn(f"found errors for functions: {errors}")
		if errors:
			build_error_file(errors)
			show_errors_file()
		if not is_strict() and not errors and not self.missing:
			print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'")
		return errors
