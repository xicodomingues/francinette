from distutils import command
import io
import logging
import os
import re
import subprocess
from typing import List
from utils.ExecutionContext import BONUS_FUNCTIONS, PART_1_FUNCTIONS, PART_2_FUNCTIONS
from testers.libft.BaseExecutor import remove_ansi_colors

from halo import Halo
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

		Halo(f"{CT.CYAN}Executing: {CT.B_WHITE}{self.folder}{CT.NC} ({self.git_url})").info()

		command = self.get_command()
		logger.info(f'executing: {command}')
		proc = subprocess.Popen(command, shell=True)
		proc.wait()
		with open("war-machine.stdout") as out:
			res = [remove_ansi_colors(line) for line in out.readlines()]
			logger.info(res)
			return res

	def get_command(self):
		to_execute_set = set(self.to_execute);
		part1_inter = to_execute_set.intersection(PART_1_FUNCTIONS)
		part2_inter = to_execute_set.intersection(PART_2_FUNCTIONS)
		bonus_inter = to_execute_set.intersection(BONUS_FUNCTIONS)

		logger.info(f"part1_funcs: {part1_inter}")
		logger.info(f"part2_funcs: {part2_inter}")
		logger.info(f"bonus_funcs: {bonus_inter}")

		if len(self.to_execute) <= 10:
			funcs = [f"ft_{func}" for func in self.to_execute]
			return f"./grademe.sh -l {' '.join(funcs)} | tee war-machine.stdout"

		if (len(part1_inter) == len(PART_1_FUNCTIONS)
				and len(part2_inter) > 0
				and len(bonus_inter) == 0):
			return f"./grademe.sh -b -m | tee war-machine.stdout"

		if (len(part1_inter) > 0
				and len(part2_inter) == 0
				and len(bonus_inter) == 0):
			return f"./grademe.sh -op1 -m | tee war-machine.stdout"
		return f"./grademe.sh -m | tee war-machine.stdout"

	def parse_output(self, output):

		def is_func(line: str):
			return func_line_regex.match(line)

		def parse_func(line: str):
			match = func_line_regex.match(line)
			return (match.group(1), match.group(2))

		parsed = [parse_func(line) for line in output if is_func(line)]
		return [func for func, res in parsed if res != "OK"]
