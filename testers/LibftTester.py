import logging
import os
import re
import shutil
import subprocess
from collections import namedtuple
from main import CT, TestRunInfo
from testers.CommonTester import show_banner
from testers.libft.ExecuteFsoares import ExecuteFsoares
from testers.libft.ExecuteTripouille import ExecuteTripouille

logger = logging.getLogger()

Tester = namedtuple("Test", "name constructor")

AVAILABLE_TESTERS = [Tester('Tripouille', ExecuteTripouille)]  # ,Tester('fsoares', ExecuteFsoares)]

FUNCTIONS_UNDER_TEST = [
    "isalpha", "isdigit", "isalnum", "isascii", "isprint", "strlen", "memset", "bzero", "memcpy", "memmove", "strlcpy",
    "strlcat", "toupper", "tolower", "strchr", "strrchr", "strncmp", "memchr", "memcmp", "strnstr", "atoi", "calloc",
    "strdup", "substr", "strjoin", "strtrim", "split", "itoa", "strmapi", "striteri", "putchar_fd", "putstr_fd",
    "putendl_fd", "putnbr_fd"
]


def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3


def run_command(command: str):
	to_execute = command.split(" ")
	print(f"{CT.CYAN}Executing: {CT.WHITE}{' '.join(to_execute)}{CT.NC}: ", end='')
	process = subprocess.run(to_execute, capture_output=True, text=True)

	if process.returncode == 0:
		print(f"{CT.L_GREEN}OK!{CT.NC}")
	else:
		print(f"{CT.L_RED}KO!{CT.NC}")
		print(process.stderr)
		raise Exception("Problem creating the library")
	return process


func_regex = re.compile(r"\w+\s+\*?ft_(\w+)\(.*")
norm_func_regex = re.compile(r"^([\w\\]+\.c): Error!")


class LibftTester():

	def __init__(self, info: TestRunInfo) -> None:
		if info.verbose:
			logger.setLevel("INFO")

		show_banner("libft")
		self.temp_dir = info.temp_dir
		self.tests_dir = info.tests_dir
		self.source_dir = info.source_dir

		self.prepare_ex_files()
		norm_res = self.check_norminette()
		compile_res = self.create_library()

		present = self.get_present()
		to_execute = intersection(present, FUNCTIONS_UNDER_TEST)

		if info.ex_to_execute:
			to_execute = info.ex_to_execute

		missing = [f for f in FUNCTIONS_UNDER_TEST if f not in to_execute]
		logger.info(f"To execute: {to_execute}")
		logger.info(f"Missing: {missing}")

		for tester in AVAILABLE_TESTERS:
			funcs_error = self.test_using(info, to_execute, missing, tester)
			if not info.ex_to_execute:
				self.show_summary(norm_res, present, missing, funcs_error)

	def test_using(self, info: TestRunInfo, to_execute, missing, tester: Tester):
		self.prepare_tests(tester.name)

		if info.ex_to_execute:
			tx = tester.constructor(self.tests_dir, info.temp_dir, info.ex_to_execute, missing)
			tx.execute()
		else:
			present = self.get_present()
			to_execute = intersection(present, FUNCTIONS_UNDER_TEST)

			tx = tester.constructor(self.tests_dir, info.temp_dir, to_execute, missing)
			return tx.execute()

	def show_summary(self, norm: str, present, missing, errors):

		def get_norm_errors():

			def get_fname(line):
				return norm_func_regex.match(line).group(1)

			def is_file(line):
				return norm_func_regex.match(line)

			return [get_fname(line) for line in norm.splitlines() if is_file(line)]

		norm_errors = get_norm_errors()
		if norm_errors:
			print(f"{CT.L_RED}Norminette Errors:{CT.NC}")
			print(', '.join(norm_errors))

		if missing:
			print(f"\n{CT.L_RED}Missing functions: {CT.NC}{', '.join(missing)}")

		if errors:
			print(f"\n{CT.L_RED}Failed tests: {CT.NC}{', '.join(errors)}")

		if not missing and not norm_errors and not errors:
			print(f"🎉🥳 {CT.L_GREEN}All tests passed! Congratulations!{CT.NC} 🥳🎉")

	def prepare_ex_files(self):
		if os.path.exists(self.temp_dir):
			logger.info(f"Removing already present directory {self.temp_dir}")
			shutil.rmtree(self.temp_dir)

		# os.makedirs(self.temp_dir)
		shutil.copytree(self.source_dir, self.temp_dir)

	def check_norminette(self):
		os.chdir(os.path.join(self.temp_dir))
		logger.info(f"On directory {os.getcwd()}")
		logger.info(f"Executing norminette")
		norm_exec = ["norminette", "-R", "CheckForbiddenSourceHeader"]

		result = subprocess.run(norm_exec, capture_output=True, text=True)

		print(f"{CT.CYAN}\nExecuting: {CT.WHITE}{' '.join(norm_exec)}{CT.NC}: ", end="")
		if result.returncode != 0:
			print(f"{CT.L_RED}KO!{CT.NC}")
			print(f"{CT.YELLOW}{result.stdout}{CT.NC}")
		else:
			print(f"{CT.L_GREEN}OK!{CT.NC}")

		return result.stdout

	def create_library(self):
		logger.info(f"Calling make on directory {os.getcwd()}")

		run_command("make fclean")
		run_command("make")


	def prepare_tests(self, testname):
		# delete destination folder if already present
		temp_dir = os.path.join(self.temp_dir, testname)
		if os.path.exists(temp_dir):
			logger.info(f"Removing already present directory {temp_dir}")
			shutil.rmtree(temp_dir)

		# copy test framework
		tester_dir = os.path.join(self.tests_dir, testname)
		logger.info(f"Copying from {tester_dir} to {temp_dir}")
		shutil.copytree(tester_dir, temp_dir)

		# copy compiled library
		library = os.path.join(self.temp_dir, "libft.a")
		if not os.path.exists(library):
			raise Exception(f"{CT.L_RED}libft.a{CT.RED} was not created. " + "Please create it in the Makefile.")
		logger.info(f"Copying libft.a from {library} to {temp_dir}")
		shutil.copy(library, temp_dir)

		# copy header
		header = os.path.join(self.temp_dir, "libft.h")
		logger.info(f"Copying libft.h from {header} to {temp_dir}")
		shutil.copy(header, temp_dir)

		return True

	def get_present(self):
		header = os.path.join(self.temp_dir, "libft.h")
		if not os.path.exists(header):
			raise Exception(f"There is no {CT.L_RED}libft.h{CT.RED} present")
		with open(header, "r") as h:
			funcs_str = [line for line in h.readlines() if func_regex.match(line)]
			return [func_regex.match(line).group(1) for line in funcs_str]
