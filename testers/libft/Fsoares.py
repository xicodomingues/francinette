import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from pipes import quote
from tempfile import tempdir
from typing import Set

from halo import Halo
from pexpect import run
from testers.libft.BaseExecutor import remove_ansi_colors
from utils.ExecutionContext import get_timeout, has_bonus, is_strict
from utils.TerminalColors import TC
from utils.Utils import is_linux, is_mac, open_ascii, show_errors_file
from utils.TraceToLine import program_name_start

logger = logging.getLogger("fsoares")

test_regex = re.compile(r"ft_(\w+)\s*: (.*)")
trace_regex = re.compile(r"\d+\s+[\w.?]+\s+[\d\w]+ (\w+) \+ (\d+)")
lldb_out_regex = re.compile(r"\s+Summary: test_\w+.out`(\w+) \+ (\d+) at (.*)$")
errors_color_name = "errors_color.log"


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

	def recompile_with_sanitizer(self):
		other_dir = Path(self.temp_dir, "..", "__my_srcs")
		makefile = Path(other_dir, "Makefile").resolve()
		with open(makefile, 'r') as file:
			filedata = file.read()
		new_make = re.sub(r"-\bWall\b", f"-g -fsanitize=address -Wall", filedata)
		if is_linux():
			new_make = re.sub(r"-\bWall\b", f"-g -Wall", filedata)
		logger.info("added sanitization to makefile")
		with open(makefile, 'w') as file:
			file.write(new_make)

		os.chdir(other_dir)
		command = "make re" + (" bonus" if has_bonus() else "")
		logger.info(f"Calling '{command}' on directory {os.getcwd()}")

		to_execute = command.split(" ")
		process = subprocess.run(to_execute, capture_output=True, text=True)
		logger.info(process)

		if process.returncode == 0:
			logger.info(f"copying sanitized libft.a from {other_dir} to {self.temp_dir}")
			shutil.copy(other_dir / "libft.a", Path(self.temp_dir, "libft.a"))

	def compile_test(self):
		text = f"{TC.CYAN}Compiling tests: {TC.B_WHITE}{self.folder}{TC.NC} (my own)"
		with Halo(text=text) as spinner:
			self.recompile_with_sanitizer()

			os.chdir(self.temp_dir)
			logger.info(f"On directory {os.getcwd()}")

			for func in self.to_execute:
				strict = "-DSTRICT_MEM" if is_strict() else ""
				bonus = " list_utils.c" if has_bonus() else ""
				sanitize = "-fsanitize=address" if is_mac() else ""
				command = (
				    f"gcc -g {sanitize} {strict} -D TIMEOUT={get_timeout()} -Wall -Wextra -Werror -Wno-deprecated-declarations my_utils.c {bonus} "
				    + f"test_{func}.c utils/malloc_mock.c utils/utils.c -L. -lft -o test_{func}.out -ldl")
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

		def parse_sanitizer(func, output: str):
			if not output.startswith("================================="):
				return output

			error = []
			for line in output.splitlines(keepends=True):
				error.append(line)
				if line.startswith("SUMMARY: AddressSanitizer:"):
					break
			with open(f"errors_{func}.log", "a") as err_file:
				err_file.writelines(error)
				err_file.write("\n")
			return "".join(output.splitlines(keepends=True)[-2:])

		def get_output(func, output):
			new_output = parse_sanitizer(func, output)
			spinner.stop()
			print(new_output, end="")
			return output

		def execute_test(func):
			spinner.start(f"ft_{func.ljust(13)}:")
			out, code = run("sh -c " + quote(f'./test_{func}.out'), withexitstatus=1)
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
			with open(errors_color_name, "w") as error_log:
				for func in errors:
					path = Path(self.tests_dir, f"test_{func}.c").resolve()
					error_log.write(program_name_start + f"test_{func}.out\n")
					error_log.write(f"For {TC.CYAN}ft_{func}{TC.NC}, in {TC.B_WHITE}{path}{TC.NC}:\n\n")
					with open_ascii(f"errors_{func}.log", "r") as f_error:
						error_log.write(f_error.read())

		errors = []
		for func, res, lines in output:
			if (is_error(res)):
				errors.append(func)
		logger.warn(f"found errors for functions: {errors}")
		if errors:
			build_error_file(errors)
			show_errors_file(Path(self.temp_dir), "errors_color.log", "error.log")
		if not is_strict() and not errors and not self.missing:
			print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'. " +
				"Moulinette will not do these checks, it's only a matter of pride!")
		return errors
