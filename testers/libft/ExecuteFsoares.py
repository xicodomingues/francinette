

import fileinput
import logging
import os
import subprocess
from typing import List
from main import CT
from testers.libft.BaseExecutor import BaseExecutor, remove_ansi_colors

logger = logging.getLogger()


class ExecuteFsoares(BaseExecutor):

	def __init__(self, tests_dir, temp_dir, to_execute: List[str], missing) -> None:
		self.folder = "fsoares"
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)
		self.git_url = None

	def execute(self):
		self.prepare_tests()
		self.compile_test()
		self.execute_tests()

	def prepare_tests(self):

		def create_test_header():
			logger.info("Writting the test.h")
			with open("tests.h", 'w') as f:
				for test in self.to_execute:
					f.write(f"#define TEST_{test.upper()}\n")

		def replace_line(line):
			for test in self.missing:
				line = line.replace(f"\ttest({test})", f"//\ttest({test})")  \
						   .replace(f"create_test({test})", f"//create_test({test})")
			return line

		os.chdir(self.temp_dir)
		logger.info(f"On {os.getcwd()}")
		create_test_header()

		logger.info("Commenting tests")

		with fileinput.FileInput("main.c", inplace=True) as file:
			for line in file:
				print(replace_line(line), end='')

	def compile_test(self):
		self.compile_with("gcc -Wall -Wextra -I. main.c print_mem.c -L. -lft")

	def execute_tests(self):
		execute = ["./a.out"]
		print(f"\n{CT.CYAN}Executing: {CT.WHITE}{' '.join(execute)}{CT.NC}:")

		p = subprocess.run(execute, capture_output=True, text=True)
		print(p.stdout, CT.NC)

		return [remove_ansi_colors(line) for line in p.stdout.splitlines()]