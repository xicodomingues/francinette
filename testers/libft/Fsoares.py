import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from pipes import quote
from typing import Set

from halo import Halo
from pexpect import run
from testers.libft.BaseExecutor import remove_ansi_colors
from utils.ExecutionContext import get_timeout, has_bonus, is_strict
from utils.TerminalColors import TC
from utils.Utils import open_ascii

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
		new_make = re.sub(r"-\bWall\b", f"-gfull '-fsanitize=address' -Wall", filedata)
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
				command = (f"gcc -gfull -fsanitize=address {strict} -D TIMEOUT={get_timeout()} -Wall -Wextra -Werror utils.c{bonus} " +
				           f"test_{func}.c malloc_mock.c -L. -lft -o test_{func}.out -ldl")
				logger.info(f"executing {command}")
				res = subprocess.run(command, shell=True, capture_output=True, text=True)
				logger.info(res)
				if res.returncode != 0:
					spinner.fail()
					print(res.stderr)
					raise Exception("Problem compiling the tests")
			spinner.succeed()

	def parse_lldb_out(self, lldb_out: str):

		def get_file_line(line):
			match = lldb_out_regex.match(line)
			if match:
				return "in " + match.group(1) + " " + match.group(3)

		stack_traces = []
		temp = []
		highlight_next = False
		for line in [get_file_line(line) for line in lldb_out.splitlines()]:
			if line:
				if "_add_malloc" in line:
					if temp:
						stack_traces.append(temp)
					temp = []
				if highlight_next:
					line = TC.YELLOW + "  -> " + line + TC.NC
					highlight_next = False
				else:
					line = "     " + line
				if line.startswith("     in malloc "):
					highlight_next = True
				temp.append(line + '\n')
		if temp:
			stack_traces.append(temp)
		logger.info(stack_traces)
		return stack_traces

	def add_to_error_file(self, func, traces):
		result = []
		i = 0
		error_file = Path(self.temp_dir, f"errors_{func}.log")
		with open(error_file) as err:
			for error in err.readlines():
				result.append(error)
				if error.startswith("Memory leak:"):
					result += traces[i]
					i += 1
		with open(error_file, 'w') as err:
			err.writelines(result)

	def add_leak_stack_trace(self, func):

		def transform(line):
			match = trace_regex.match(line)
			if match:
				if match.group(1) == "0x0" or (match.group(1) == "start" and match.group(2) == "1"):
					return ''
				return f"image lookup --address {match.group(1)}+{match.group(2)}\n"
			return '\n'

		with open(Path(self.temp_dir, "backtrace")) as bf:
			lines = bf.readlines()
		lines = [transform(line) for line in lines]
		with open(Path(self.temp_dir, "lldb_commands"), 'w') as lldbf:
			lldbf.writelines(lines)
		p = subprocess.run(f"lldb test_{func}.out -s lldb_commands --batch", shell=True, capture_output=True, text=True)
		logger.info(p)
		traces = self.parse_lldb_out(p.stdout)
		self.add_to_error_file(func, traces)

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
			return output.splitlines(True)[-1]

		def get_output(func, output):
			new_output = parse_sanitizer(func, output)
			spinner.stop()
			print(new_output, end="")
			return output

		def execute_test(func):
			spinner.start(f"ft_{func.ljust(13)}:")
			out, code = run("sh -c " + quote(f'./test_{func}.out'),
			                withexitstatus=1)  # ASAN_OPTIONS="log_path=asan.log"
			output = out.decode('ascii', errors="backslashreplace")
			logger.info(output)
			output = get_output(func, output)
			self.add_leak_stack_trace(func)
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
					error_log.write(f"For {TC.CYAN}ft_{func}{TC.NC}, in {TC.B_WHITE}{path}{TC.NC}:\n\n")
					with open_ascii(f"errors_{func}.log", "r") as f_error:
						error_log.write(f_error.read())

		def show_errors_file():
			file = Path(self.temp_dir, errors_color_name)
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
