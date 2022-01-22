import logging
import os
import re
import subprocess
from typing import List
from testers.libft.BaseExecutor import remove_ansi_colors

from utils.TerminalColors import CT

logger = logging.getLogger("war-machine")


func_line_regex = re.compile(r"^ft_(\w+).*(OK|KO)$")


class ExecuteWarMachine():

	def __init__(self, tests_dir, temp_dir, to_execute: List[str], missing) -> None:
		self.folder = "war-machine"
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)
		self.git_url = "https://github.com/y3ll0w42/libft-war-machine"

	def execute(self):
		output = self.execute_tests()
		return self.parse_output(output)

	def execute_tests(self):
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()} Executing war-machine")

		print(f"{CT.CYAN}Executing: {CT.B_WHITE}{self.folder}{CT.NC} ({self.git_url})")
		proc = subprocess.Popen("./grademe.sh -ob -m | tee war-machine.stdout", shell=True)
		proc.wait()
		with open("war-machine.stdout") as out:
			return [remove_ansi_colors(line) for line in out.readlines()];

	def parse_output(self, output):
		def is_func(line: str):
			return func_line_regex.match(line)

		def parse_func(line: str):
			match = func_line_regex.match(line)
			return (match.group(1), match.group(2))

		parsed = [parse_func(line) for line in output if is_func(line)]
		return [func for func, res in parsed if res != "OK"]
