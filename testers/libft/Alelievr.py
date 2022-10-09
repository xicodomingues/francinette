
import logging
import os
from pathlib import Path
import re
import subprocess
from sys import platform
from halo import Halo
from typing import List
from testers.libft.BaseExecutor import BONUS_FUNCTIONS
from utils.ExecutionContext import get_timeout, has_bonus

from utils.TerminalColors import TC
from utils.Utils import decode_ascii, open_ascii

logger = logging.getLogger("alelievr")

func_regex = re.compile(r'^\s+\{"ft_(\w+)",.*')
out_func_line = re.compile(r'^ft_(\w+):.*')

class Alelievr():

	name = "libft-unit-test"
	folder = "alelievr"
	git_url = "https://github.com/alelievr/libft-unit-test"

	def __init__(self, tests_dir, temp_dir, to_execute: List[str], missing) -> None:
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = list(missing)
		self.tests_dir = os.path.join(tests_dir, self.folder)

		if not has_bonus():
			self.missing += BONUS_FUNCTIONS

	def execute(self):
		self.prepare_tests()
		return self.execute_tester()

	def prepare_tests(self):
		def handle_line(line: str):
			match = func_regex.match(line)
			if (match and match.group(1) in self.missing):
				return "//" + line
			return line

		init = Path(self.temp_dir, 'src', 'init.c')
		with open(init, 'r') as f_init:
			lines = [handle_line(line) for line in f_init.readlines()]
		with open(init, 'w') as f_init:
			f_init.writelines(lines)

		if platform == "linux" or platform == "linux2":
			with open(Path(self.temp_dir, "..", "__my_srcs", "Makefile"), 'a') as mf:
				mf.writelines("\n\nso:\n\tgcc -nostartfiles -shared -o libft.so *.o\n")

	def execute_tester(self):
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()} Executing alelievr")

		text = f"{TC.CYAN}Compiling tests: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})"
		with Halo(text) as spinner:
			p = subprocess.run(["make", f"TIMEOUT={get_timeout() * 1_000}" , "all"], capture_output=True)
			logger.info(p)
			if p.returncode != 0:
				error = p.stderr.decode('ascii', errors="backslashreplace")
				spinner.fail()
				print(error)
				raise Exception("Problem compiling tests")
			spinner.succeed()
		Halo(text=f"{TC.CYAN}Testing:{TC.NC}").info()
		p = subprocess.Popen("./run_test", stdout=subprocess.PIPE)
		for line in p.stdout:
			line_str = decode_ascii(line).rstrip()
			print(line_str)

		logger.info(p)
		return self.parse_output()

	def parse_output(self):
		def is_error(line):
			if out_func_line.match(line):
				for test in re.finditer(r"\[([^\]]+)\]", line):
					if test.group(1) != 'OK':
						return True
			return False

		def show_file_output(path):
			with open_ascii(path) as file:
				error_lines = [line for line in file.readlines() if not out_func_line.match(line)]
				print(" ".join(error_lines[:50]), end="")
				if (len(error_lines) > 50):
					print(f"...\n\nFile too large. To see full report open: {TC.PURPLE}{log_path}{TC.NC}\n")

		log_path = Path(self.temp_dir, 'result.log')
		with open_ascii(log_path) as file:
			errors = [out_func_line.match(line).group(1) for line in file.readlines() if is_error(line)]
			if len(errors) > 0:
				show_file_output(log_path)
			return errors