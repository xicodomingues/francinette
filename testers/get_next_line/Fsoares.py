import logging
import re
from typing import Set

from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_timeout, has_bonus, is_strict
from utils.TerminalColors import TC
from utils.Utils import show_errors_file

logger = logging.getLogger("gnl-fsoares")

buffer_size_regex = re.compile(r"BUFFER_SIZE: (\d+)")


class Fsoares(BaseExecutor):

	name = 'fsoares'
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):

		bonus_tests = ["open, close, open", "2 file descriptors", "multiple fds", "test limit fds"]

		def execute_command(command, execute=True, silent=False):
			if not execute:
				return []
			strict = "EXEC_STRICT=1" if is_strict() else ""
			command = f"{command} {strict}"
			logger.info(f"executing: {command}")
			output = self.run_tests(command, show_message=not silent)
			logger.info(output)
			return list(self.check_errors(output))

		def validate_one_static():
			static_regex = re.compile(r".*static.*;.*")
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
				show_errors_file(self.temp_dir / "error_color.log", self.temp_dir / "errors.log")

			self.show_test_files(errors, bonus_tests, "tester.c", "bonus.c")
			if has_bonus() and self.exec_bonus:
				if not validate_one_static():
					errors.add("more than one static")
			if not is_strict() and not errors:
				print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'. " +
				      f"Moulinette will not do these checks, it's only a matter of pride.")
			return errors

		timeout = f"TIMEOUT={get_timeout()}"
		errors = execute_command(f"make {timeout} mandatory", self.exec_mandatory)
		bonus_errors = set(errors).union(execute_command(f"make {timeout} bonus", self.exec_bonus, True))
		bonus_errors = show_errors(bonus_errors)
		return [self.name] if bonus_errors else []
