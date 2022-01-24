
import logging
import os
import subprocess
from halo import Halo
from typing import List

from utils.TerminalColors import TC

logger = logging.getLogger("alelievr")

class ExecuteAlelievr():

	def __init__(self, tests_dir, temp_dir, to_execute: List[str], missing) -> None:
		self.folder = "alelievr"
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)
		self.git_url = "https://github.com/alelievr/libft-unit-test"

	def execute(self):
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
		return []