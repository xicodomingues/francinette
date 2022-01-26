import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
from dataclasses import dataclass

from utils.ExecutionContext import TestRunInfo
from utils.TerminalColors import TC
from utils.Utils import show_banner

logger = logging.getLogger("cpiscine")

DEFAULT_COMPILE_FLAGS = ["-Wall", "-Wextra", "-Werror"]
IGNORED_EXERCISE_HEADER = f"{TC.YELLOW}" \
        "═════════════════════════════════ #### ignored ═════════════════════════════════" \
        f"{TC.NC}"

EXERCISE_HEADER = f"{TC.B_BLUE}" \
        "═════════════════════════════════ Testing #### ═════════════════════════════════" \
        f"{TC.NC}"

TEST_PASSED = f"\n{TC.B_GREEN}" \
        "══════════════════════════════    #### passed!    ══════════════════════════════" \
        f"{TC.NC}"

TEST_FAILED = f"\n{TC.B_RED}" \
        "══════════════════════════════    #### failed!    ══════════════════════════════" \
        f"{TC.NC}"

TEST_NOT_PRESENT = f"\n{TC.YELLOW}" \
        "══════════════════════════════  #### not present  ══════════════════════════════" \
        f"{TC.NC}"

TEST_ONLY_EXECUTED = f"\n{TC.PURPLE}" \
        "══════════════════════════════   ####  executed   ══════════════════════════════" \
        f"{TC.NC}"


@dataclass
class VeriOut:
	returncode: int
	stdout: str


class CommonTester:

	def __init__(self, info: TestRunInfo):
		self.compile_flags = []
		self.exercise_files = []
		self.test_files = []
		self.compile = []
		self.norm_ignore = []
		self.temp_dir = info.base_dir / "temp" / self.name
		self.tests_dir = info.base_dir / "tests" / "cpiscine" / self.name
		self.source_dir = info.source_dir
		self.selected_test = info.ex_to_execute

		if self.selected_test:
			test = "ex" + self.selected_test[0].ljust(2, '0')[-2:]
			test_ok = self.execute_test(test)
			self.show_result(test, test_ok)
			return

		self.available_tests = [test for test in dir(self) if re.match(r"^ex\d{2}$", test)]
		logger.info("tests found: %s", self.available_tests)

		show_banner(self.name)

		test_status = {}
		for test in self.available_tests:
			test_ok = self.execute_test(test)
			test_status[test] = test_ok
			self.show_result(test, test_ok)

			print("\n")
			self.clean_up()

		self.print_summary(test_status)

	@staticmethod
	def show_result(test, test_ok):
		if test_ok:
			print(TEST_PASSED.replace("####", test.title()))
		elif not test_ok:
			print(TEST_FAILED.replace("####", test.title()))
		elif test_ok == "Test Not Present":
			print(TEST_NOT_PRESENT.replace("####", test.title()))
		elif test_ok == "No expected file":
			print(TEST_ONLY_EXECUTED.replace("####", test.title()))

	@staticmethod
	def print_summary(test_status):
		ok_tests = [test for test, st in test_status.items() if st is True]

		print(f"{TC.B_GREEN}Passed tests: {' '.join(ok_tests)}{TC.NC}")
		failed_tests = [test for test, st in test_status.items() if st is False]
		if failed_tests:
			print(f"{TC.B_RED}Failed tests: {' '.join(failed_tests)}{TC.NC}")
		not_present = [test for test, st in test_status.items() if st == "Test Not Present"]
		if not_present:
			print(f"{TC.YELLOW}Files not present: {' '.join(not_present)}{TC.NC}")
		not_present = [test for test, st in test_status.items() if st == "No expected file"]
		if not_present:
			print(f"{TC.PURPLE}Need manual validation: {' '.join(not_present)}{TC.NC}")

	def pass_norminette(self, test):
		os.chdir(os.path.join(self.temp_dir, test))
		logger.info(f"On directory {os.getcwd()}")
		logger.info(f"Executing norminette on files: {self.exercise_files}")
		norm_exec = ["norminette", "-R", "CheckForbiddenSourceHeader"] + self.exercise_files

		result = subprocess.run(norm_exec, capture_output=True, text=True)

		print(f"{TC.CYAN}Executing: {TC.B_WHITE}{' '.join(norm_exec)}{TC.NC}:")
		if result.returncode == 0:
			print(f"{TC.GREEN}{result.stdout}{TC.NC}")
		else:
			print(f"{TC.YELLOW}{result.stdout}{TC.NC}")

		return result.returncode == 0

	def compile_files(self):
		files = self.test_files + self.exercise_files
		flags = self.compile_flags if self.compile_flags else DEFAULT_COMPILE_FLAGS

		logger.info(f"compiling files: {files} with flags: {flags}")
		# result = os.system(f"gcc { " ".join(flags) } { " ".join(files) }")
		gcc_exec = ["gcc"] + flags + files

		print(f"{TC.CYAN}Executing: {TC.B_WHITE}{' '.join(gcc_exec)}{TC.NC}:")
		p = subprocess.Popen(gcc_exec)
		p.wait()

		if p.returncode == 0:
			print(f"{TC.GREEN}gcc: OK!{TC.NC}")
		else:
			print(f"{TC.B_RED}Problem compiling files{TC.NC}")

		return p.returncode

	def execute_program(self, test):
		logger.info(f"Running the output of the compilation: ")
		logger.info(f"On directory {os.getcwd()}")

		print(f"\n{TC.CYAN}Executing: {TC.B_WHITE}./a.out | cat -e{TC.NC}:")

		ps = subprocess.Popen('./a.out', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		output = subprocess.check_output(('cat', '-e'), stdin=ps.stdout)
		ps.wait()
		output = output.decode('ascii', errors="backslashreplace")

		if ps.returncode == 0:
			logger.info("Executed program successfully main")
			print(output)
		else:
			print(f"{TC.RED}{output}{TC.NC}")
			print(f"{TC.B_RED}Error Executing the program! (Most likely SegFault){TC.NC}")
			location = os.path.join(self.temp_dir, test)
			print(f"The {TC.B_WHITE}main.c{TC.NC} and {TC.B_WHITE}a.out{TC.NC} used in this "
			      f"test are located at:\n{TC.B_WHITE}{location}{TC.NC}")

		return output

	@staticmethod
	def do_diff():
		diff_exec = ["diff", "--text", "expected", "out"]
		print(f"\n{TC.CYAN}Executing: {TC.B_WHITE}{' '.join(diff_exec)}{TC.NC}:")

		result = subprocess.run(diff_exec, capture_output=True, text=True)
		if result.returncode == 0:
			print(f"{TC.GREEN}diff: No differences{TC.NC}")
		else:
			print(f"{TC.B_PURPLE}< expected, > your result{TC.NC}")
			print(f"{TC.RED}{result.stdout}{TC.NC}")

		return result.returncode == 0

	@staticmethod
	def do_verification_fn(verification_fn):
		print(f"\n{TC.CYAN}Executing function: {TC.B_WHITE}{verification_fn.__name__}{TC.NC}:")

		result = verification_fn()
		if result.returncode == 0:
			print(f"{TC.GREEN}Everything OK!{TC.NC}")
		else:
			print(f"{TC.RED}{result.stdout}{TC.NC}")

		return result.returncode == 0

	def compare_with_expected(self, output, test):
		expected_file = os.path.join(os.getcwd(), 'expected')

		if not os.path.exists(expected_file):
			return "No expected file"

		out_file_path = os.path.join(os.getcwd(), 'out')

		logger.info(f"Creating out file: {out_file_path} with content {output}")
		with open(out_file_path, 'w') as out_file:
			out_file.write(output)
			out_file.close()

			verification_fn = getattr(self, f"{test}_verification", None)
			if verification_fn:
				return self.do_verification_fn(verification_fn)
			else:
				return self.do_diff()

	def execute_test(self, test_to_execute):
		logger.info(f"starting execution of {test_to_execute}")

		print(EXERCISE_HEADER.replace("####", test_to_execute))
		print()
		getattr(self, test_to_execute)()

		logger.info("Preparing the test")
		ready = self.prepare_test(test_to_execute)
		if not ready:
			return "Test Not Present"

		norm_passed = self.pass_norminette(test_to_execute)
		status = self.compile_files()
		if status != 0:
			return False

		output = self.execute_program(test_to_execute)
		return norm_passed and self.compare_with_expected(output, test_to_execute)

	def prepare_test(self, test):
		try:
			# delete destination folder if already present
			temp_dir = os.path.join(self.temp_dir, test)
			if os.path.exists(temp_dir):
				logger.info(f"Removing already present directory {temp_dir}")
				shutil.rmtree(temp_dir)

			os.makedirs(temp_dir)

			# copy exercise files from source folder
			for filename in self.exercise_files:
				source_path = os.path.join(self.source_dir, test, filename)
				dest_path = os.path.join(temp_dir, filename)
				logger.info(f"Copying source file: {source_path} to {dest_path}")
				shutil.copy(source_path, dest_path)

			# copy files from test folder and the expected files
			for filename in self.test_files:
				source_path = os.path.join(self.tests_dir, test, filename)
				dest_path = os.path.join(temp_dir, filename)
				logger.info(f"Copying test file: {source_path} to {dest_path}")
				shutil.copy(source_path, dest_path)

			expected_path = os.path.join(self.tests_dir, test, "expected")
			if os.path.exists(expected_path):
				logger.info(f"Copying expected file: {expected_path} to {temp_dir}")
				shutil.copy(expected_path, temp_dir)

			# remove a.out
			program_path = os.path.join(self.tests_dir, test, "a.out")
			if os.path.exists(program_path):
				logger.info(f"Removing file: {program_path}")
				shutil.rmtree(program_path)

			# remove out
			program_path = os.path.join(self.tests_dir, test, "out")
			if os.path.exists(program_path):
				logger.info(f"Removing file: {program_path}")
				shutil.rmtree(program_path)

			return True
		except Exception as ex:
			logger.info("Problem creating the files structure: ", ex)
			return False

	def clean_up(self):
		self.compile_flags = []
		self.compile = []
		self.norm_ignore = []
