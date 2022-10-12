import logging
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List

from halo import Halo
from testers.libft.BaseExecutor import (BONUS_FUNCTIONS, PART_1_FUNCTIONS,
                                        PART_2_FUNCTIONS, remove_ansi_colors)
from utils.ExecutionContext import get_timeout
from utils.TerminalColors import TC
from utils.Utils import intersection

logger = logging.getLogger("war-machine")

func_line_regex = re.compile(r"^ft_(\w+)\s*([^ ]+)\s*(OK|KO)$")
lines_finder = re.compile(r'(^.*if.*atoi\(argv\[1\]\).* == \d.*$)|(^\s+else if \(arg == \d+\).*$)')


def cat_file(path):
	p = subprocess.run(f'cat -e {path.resolve()}', shell=True, capture_output=True)
	print(p.stdout.decode('ascii', errors="backslashreplace"), end='')


class WarMachine():

	name = "libft-war-machine"
	folder = "war-machine"
	git_url = "https://github.com/y3ll0w42/libft-war-machine"

	def __init__(self, tests_dir, temp_dir, to_execute: List[str], missing) -> None:
		self.temp_dir = os.path.join(temp_dir, self.folder)
		self.to_execute = to_execute
		self.missing = missing
		self.tests_dir = os.path.join(tests_dir, self.folder)

	def execute(self):
		output = self.execute_tests()
		return self.parse_output(output)

	def execute_tests(self):
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()} Executing war-machine")

		Halo(f"{TC.CYAN}Executing: {TC.B_WHITE}{self.name}{TC.NC} ({self.git_url})").info()

		command = self.get_command()
		logger.info(f'executing: {command}')
		proc = subprocess.Popen(['/bin/bash', '-c', command])
		proc.wait()
		with open("war-machine.stdout") as out:
			res = [remove_ansi_colors(line) for line in out.readlines()]
			logger.info(res)
			print(TC.NC)
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
		        f"{force_makefile} {get_timeout()} | tee war-machine.stdout")

	def show_failed_test_code(self, func, tests):

		def get_part(func):
			if func in PART_1_FUNCTIONS:
				return "Part1_functions"
			if func in PART_2_FUNCTIONS:
				return "Part2_functions"
			if func in BONUS_FUNCTIONS:
				return "Bonus_functions"

		def print_test_lines(lines, start, number):
			tabs = lines[start + 1].count('\t')
			print(f"{TC.BLUE}Test {number + 1}{TC.NC}:")
			if not re.match(r'\t+\{', lines[start + 1]):
				print(lines[start + 1][tabs - 1:].replace('\t', " " * 4), end="")
				return
			i = start + 2
			while (not re.match('\t' * tabs + '}', lines[i])):
				print(lines[i][tabs:].replace("\t", " " * 4), end='')
				i += 1

		def print_diffs(path, fail):
			name = f"test{str(fail + 1).zfill(2)}"
			expected = path / '..' / f'{name}.output'
			result = path / '..' / f'user_output_{name}'

			print(f"{TC.YELLOW}Expected{TC.NC} (cat -e {name}.output):")
			cat_file(expected)
			print(f"\n{TC.RED}Your result{TC.NC} (cat -e user_output_{name}):")
			cat_file(result)
			print()

		def show_code(path, failed):
			with open(path) as mc:
				lines = mc.readlines()
			test_lines = [i for i, line in enumerate(lines) if lines_finder.match(line)]
			for fail in failed:
				print_test_lines(lines, test_lines[fail], fail)
				print_diffs(path, fail)

		path = Path(self.temp_dir, 'tests', get_part(func), f'ft_{func}').resolve()
		print(f"{TC.B_RED}Errors{TC.NC} in {TC.BLUE}{func}{TC.NC}: {TC.B_WHITE}{path}{TC.NC}")
		show_code(path / 'main.c', [i for i, test in enumerate(tests) if test != '✓'])

	def parse_output(self, output):

		def is_func(line: str):
			return func_line_regex.match(line)

		def parse_func(line: str):
			match = func_line_regex.match(line)
			if match.group(3) != "OK":
				self.show_failed_test_code(match.group(1), match.group(2))
			return (match.group(1), match.group(3))

		def print_file_summary(file):
			with open(file) as f:
				lines = f.readlines()
			print()
			[print(line, end='') for line in lines[:50]]
			if len(lines) > 50:
				dest = (file / ".." / 'errors.log').resolve()
				with open(file, "r") as orig, open(dest, "w") as log:
					log.write(remove_ansi_colors(orig.read()))
				print(f"...\n\nFile too large. To see full report open: {TC.PURPLE}{dest}{TC.NC}\n")

		orig_stdout = sys.stdout
		with open(Path(self.temp_dir, "errors_color.log"), "w") as error_log:
			sys.stdout = error_log
			parsed = [parse_func(line) for line in output if is_func(line)]
			sys.stdout = orig_stdout

		res = [func for func, res in parsed if res != "OK"]
		if len(res) != 0:
			print(f"Abort: {TC.RED}A{TC.NC}  Bus error: {TC.RED}B{TC.NC}  Segmentation fault: {TC.RED}S{TC.NC}  Timeout: {TC.RED}T{TC.NC}\n")
			longer = Path(self.temp_dir, "deepthought")
			print(f"More information in: {TC.PURPLE}{longer}{TC.NC}")
			print_file_summary(Path(self.temp_dir, 'errors_color.log'))
			#print(f"and: {TC.B_WHITE}{Path(self.temp_dir, 'errors.log').resolve()}{TC.NC}")
		return res
