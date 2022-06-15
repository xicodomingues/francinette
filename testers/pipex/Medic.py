import logging
import re
import shutil

from halo import Halo
from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import console

logger = logging.getLogger("px-medic")

test_line_regex = re.compile("^([^#]+)# (\d+):.*\[(\w+)\]$")


class Medic(BaseExecutor):

	name = 'pipexMedic'
	folder = 'pipexMedic'
	git_url = 'https://github.com/gmarcha/pipexMedic'
	line_regex = re.compile(r"^()(1\..+)$")
	test_regex = re.compile(r"(\d+)\. ([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		Halo(self.get_info_message("Executing tests")).info()
		m_errors, b_errors = False, False
		if self.exec_mandatory:
			self.execute_in_project_dir("make all")
			output = self.execute_command("bash test.sh m")
			print()
			m_errors = self.check_errors(output)
			if m_errors:
				shutil.copy("tester.log", "mandatory.log")

		if self.exec_bonus:
			console.print("[Bonus]", style="purple")
			self.execute_in_project_dir("make fclean bonus")
			output = self.execute_command("bash test.sh a")
			print()
			b_errors = self.check_errors(output)
			if b_errors:
				shutil.copy("tester.log", "bonus.log")

		if m_errors:
			self.show_errors_file("mandatory.log", "mandatory.log")
		if b_errors:
			self.show_errors_file("bonus.log", "bonus.log")
		return self.result(m_errors or b_errors)
