import logging
import re
import subprocess

from halo import Halo
from testers.BaseExecutor import BaseExecutor
from utils.Utils import show_errors_file

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
		output = self.execute_command("bash test.sh m")
		print()
		if self.check_errors(output):
			self.show_errors_file("tester.log", 30)
			return [self.name]
		return []