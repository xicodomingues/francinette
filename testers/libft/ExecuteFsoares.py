import logging
import os
import subprocess
from typing import List
from main import CT
from testers.libft.BaseExecutor import remove_ansi_colors
from halo import Halo

logger = logging.getLogger()


class ExecuteFsoares():

	def __init__(self, tests_dir, temp_dir, to_execute: List[str], missing) -> None:
		self.folder = "fsoares"
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)
		self.git_url = None

	def execute(self):
		self.compile_test()
		self.execute_tests()

	def compile_test(self):
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()}")

		text = f"{CT.CYAN}Compiling tests from: {CT.WHITE}{self.folder}{CT.NC}"
		with Halo(text=text) as spinner:
			for func in self.to_execute:
				command = f"gcc -Wall -Wextra utils.c test_{func}.c -L. -lft -o test_{func}.out"
				logger.info(f"Executing: {command}")
				res = subprocess.run(command, shell=True, capture_output=True, text=True)
				if res.returncode != 0:
					spinner.fail()
					print(res.stderr)
					raise Exception("Problem compiling the tests")

	def execute_tests(self):
		print(f"\n{CT.CYAN}Executing Tests:{CT.NC}")

		for func in self.to_execute:
			p = subprocess.run(f"./test_{func}.out", capture_output=True, text=True)
			print(p.stdout, CT.NC, end="", sep="")

		return [remove_ansi_colors(line) for line in p.stdout.splitlines()]