import re
import subprocess

from testers.BaseExecutor import BaseExecutor
from halo import Halo

from utils.Utils import show_errors_str


test_line_regex = re.compile("^([^#]+)# (\d+):.*\[(\w+)\]$")

class Vfurname(BaseExecutor):

	name = 'pipex-tester'
	folder = 'pipex-tester'
	git_url = 'https://github.com/vfurmane/pipex-tester'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		Halo(self.get_info_message("Executing tests")).info()
		proc = subprocess.Popen("./run.sh -lv", shell="True", encoding="ascii", errors="backslashreplace", stdout=subprocess.PIPE)
		output = ""
		has_errors = False
		while True:
			line = proc.stdout.readline()
			if not line:
				break
			match = test_line_regex.match(line)
			if match:
				print(f"{match.group(1)}{int(match.group(2))}.{match.group(3)} ", end="")
				if '\033[32m' not in match.group(1):
					has_errors = True
			output += line
		print("\n")
		if has_errors:
			show_errors_str(output, self.temp_dir, 20)
		return self.result(has_errors)
