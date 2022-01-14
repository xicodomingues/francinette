
from imp import init_frozen
import logging
import os
import subprocess
from typing import List
from main import CT
from testers.libft.BaseExecutor import remove_ansi_colors

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

		print(f"\n{CT.CYAN}Compiling tests from: {CT.WHITE}{self.folder}{CT.NC}", end="")
		for func in self.to_execute:
			subprocess.run(f"gcc -Wall -Wextra utils.c test_{func}.c -L. -lft", shell=True)

	def execute_tests(self):
		execute = ["./a.out"]
		print(f"\n{CT.CYAN}Executing: {CT.WHITE}{' '.join(execute)}{CT.NC}:")

		p = subprocess.run(execute, capture_output=True, text=True)
		print(p.stdout, CT.NC)

		return [remove_ansi_colors(line) for line in p.stdout.splitlines()]