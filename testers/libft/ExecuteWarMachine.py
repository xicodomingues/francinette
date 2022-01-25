from distutils import command
import io
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
from typing import List
from utils.ExecutionContext import BONUS_FUNCTIONS, PART_1_FUNCTIONS, PART_2_FUNCTIONS, intersection
from testers.libft.BaseExecutor import remove_ansi_colors

from halo import Halo
from utils.TerminalColors import TC

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

		Halo(f"{TC.CYAN}Executing: {TC.B_WHITE}{self.folder}{TC.NC} ({self.git_url})").info()

		command = self.get_command()
		logger.info(f'executing: {command}')
		proc = subprocess.Popen(['/bin/bash', '-c', command])
		proc.wait()
		with open("war-machine.stdout") as out:
			res = [remove_ansi_colors(line) for line in out.readlines()]
			logger.info(res)
			print(TC.NC);
			return res

	def get_command(self):
		part1_inter = intersection(self.to_execute, PART_1_FUNCTIONS)
		part2_inter = intersection(self.to_execute, PART_2_FUNCTIONS)
		bonus_inter = intersection(self.to_execute, BONUS_FUNCTIONS)

		logger.info(f"part1_funcs: {part1_inter}")
		logger.info(f"part2_funcs: {part2_inter}")
		logger.info(f"bonus_funcs: {bonus_inter}")

		force_makefile = " -l" if len(self.to_execute) < 5 else ""
		return (f"./my_tester.sh " +
				f"\"{' '.join(part1_inter)}\" \"{' '.join(part2_inter)}\" \"{' '.join(bonus_inter)}\"" +
				f"{force_makefile} | tee war-machine.stdout")

	def parse_output(self, output):

		def is_func(line: str):
			return func_line_regex.match(line)

		def parse_func(line: str):
			match = func_line_regex.match(line)
			return (match.group(1), match.group(2))

		parsed = [parse_func(line) for line in output if is_func(line)]
		res = [func for func, res in parsed if res != "OK"]
		if len(res) != 0:
			longer = Path(self.temp_dir, "deepthought")
			print(f"\nFor a more detailed report open: {TC.PURPLE}{longer}{TC.NC}\n")
		return res
