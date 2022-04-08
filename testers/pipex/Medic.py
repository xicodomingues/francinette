import re
import subprocess

from testers.BaseExecutor import BaseExecutor
from halo import Halo

from utils.Utils import show_errors_str


test_line_regex = re.compile("^([^#]+)# (\d+):.*\[(\w+)\]$")

class Medic(BaseExecutor):

	name = 'pipexMedic'
	folder = 'pipexMedic'
	git_url = 'https://github.com/gmarcha/pipexMedic'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		Halo(self.get_info_message("Executing tests")).info()
		subprocess.run("bash test.sh m", shell="True", encoding="ascii", errors="backslashreplace")

		return [self.name]