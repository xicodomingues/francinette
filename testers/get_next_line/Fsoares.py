import logging
import os
import re
from typing import Set

from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import has_bonus, is_strict
from utils.TerminalColors import TC
from utils.Utils import show_errors_file

logger = logging.getLogger("gnl-fsoares")

buffer_size_regex = re.compile(r"BUFFER_SIZE: (\d+)")


class Fsoares(BaseExecutor):

	name = 'fsoares'
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)(?:[^ ]+)?\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)
		# macOS: suppress inconsequential but intrusive
		# debug messages printed by Apple's libmalloc
		os.environ['MallocNanoZone'] = '0'

	def execute(self):
		bonus_tests = ["open, close, open", "2 file descriptors", "multiple fds", "test limit fds"]

		def validate_one_static():
			static_regex = re.compile(r".*\bstatic\b.*;.*")
			static_count = 0

			def count_in_file(file):
				nonlocal static_count
				with open((self.temp_dir / ".." / file).resolve()) as gnl:
					for line in gnl.readlines():
						if static_regex.match(line):
							static_count += 1

			count_in_file("get_next_line_bonus.c")
			count_in_file("get_next_line_utils_bonus.c")
			if (static_count > 1):
				print(f"{TC.RED}You have more than one {TC.B_BLUE}static{TC.RED} variable {TC.NC}")
				return False
			return True

		def show_errors(errors: Set):
			if errors:
				show_errors_file(self.temp_dir, "error_color.log", "errors.log")

			self.show_test_files(errors, bonus_tests, "tester.c", "bonus.c")
			if has_bonus() and self.exec_bonus:
				if not validate_one_static():
					errors.add("more than one static")
			if not is_strict() and not errors:
				print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'.")
			return errors

		errors = self.execute_make_command("mandatory", self.exec_mandatory)
		logger.info(f"errors: {errors}")
		bonus_errors = set(errors).union(self.execute_make_command("bonus", self.exec_bonus, True))
		bonus_errors = show_errors(bonus_errors)
		return [self.name] if bonus_errors else []
