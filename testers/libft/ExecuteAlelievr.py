
import logging
from nis import match
import os
from pathlib import Path
import re
import subprocess
from halo import Halo
from typing import List

from utils.TerminalColors import TC

logger = logging.getLogger("alelievr")

func_regex = re.compile(r'^\s+\{"ft_(\w+)",.*')
out_func_line = re.compile(r'^ft_(\w+):.*')

class ExecuteAlelievr():

	def __init__(self, tests_dir, temp_dir, to_execute: List[str], missing) -> None:
		self.folder = "alelievr"
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)
		self.git_url = "https://github.com/alelievr/libft-unit-test"

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

	def execute_tester(self):
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()} Executing war-machine")

		text = f"{TC.CYAN}Compiling tests: {TC.B_WHITE}{self.folder}{TC.NC} ({self.git_url})"
		with Halo(text) as spinner:
			p = subprocess.run("make", capture_output=True)
			logger.info(p)
			if p.returncode != 0:
				error = p.stderr.decode('ascii', errors="backslashreplace")
				spinner.fail()
				print(error)
				raise Exception("Problem compiling tests")
			spinner.succeed()
		Halo(text=f"{TC.CYAN}Testing:{TC.NC}").info()
		p = subprocess.run("./run_test")
		logger.info(p)
		print()
		return self.parse_output()

	def parse_output(self):
		def is_error(line):
			if out_func_line.match(line):
				for test in re.finditer(r"\[([^\]]+)\]", line):
					if test.group(1) != 'OK':
						return True
			return False

		log_path = Path(self.temp_dir, 'result.log')
		with open(log_path, encoding='ascii', errors="backslashreplace") as file:
			errors = [out_func_line.match(line).group(1) for line in file.readlines() if is_error(line)]
			if len(errors) > 0:
				print(f"\nFor a more detailed report open: {TC.PURPLE}{log_path}{TC.NC}\n")
			return errors