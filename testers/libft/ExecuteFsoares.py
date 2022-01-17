import logging
import os
from re import I
import re
import subprocess
from typing import List
from main import CT
from testers.libft.BaseExecutor import remove_ansi_colors
from halo import Halo

logger = logging.getLogger("fsoares")


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
		result = self.execute_tests()
		logger.info(f"result: {result}")

	def compile_test(self):
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()}")

		text = f"{CT.CYAN}Compiling tests from: {CT.WHITE}{self.folder}{CT.NC}"
		with Halo(text=text) as spinner:
			for func in self.to_execute:
				command = f"gcc -Wall -Wextra utils.c test_{func}.c -L. -lft -o test_{func}.out"
				res = subprocess.run(command, shell=True, capture_output=True, text=True)
				logger.info(res)
				if res.returncode != 0:
					spinner.fail()
					print(res.stderr)
					raise Exception("Problem compiling the tests")

	def execute_tests(self):
		print(f"\n{CT.CYAN}Testing:{CT.NC}")
		spinner = Halo(placement="right")

		def get_output(func, p):
			output = p.stdout
			if p.returncode != 0 and "Alarm clock" in p.stderr:
				output += f"ft_{func.ljust(13)}: {CT.L_YELLOW}Infinite Loop{CT.NC}\n"
			spinner.stop()
			print(output, end="")
			spinner.start()
			return output

		def execute_test(func):
			spinner.start(f"ft_{func.ljust(13)}:")
			p = subprocess.run(f"$HOME/francinette/utils/timeout.sh 3s ./test_{func}.out", capture_output=True, text=True, shell=True)
			logger.info(p)
			output = get_output(func, p);
			return [remove_ansi_colors(line) for line in output]

		result = [execute_test(func) for func in self.to_execute]
		logger.info(result)
		spinner.stop()
		return result