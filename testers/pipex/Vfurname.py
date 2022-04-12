import re
import subprocess

from halo import Halo
from utils.ExecutionContext import console
from testers.BaseExecutor import BaseExecutor
from utils.Utils import run_filter, show_errors_str

test_line_regex = re.compile("^([^#]+)# (\d+):.*\[(\w+)\]$")


class Vfurname(BaseExecutor):

	name = 'pipex-tester'
	folder = 'pipex-tester'
	git_url = 'https://github.com/vfurmane/pipex-tester'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):

		def line_handler(line):
			match = test_line_regex.match(line)
			if match:
				print(f"{match.group(1)}{int(match.group(2))}.{match.group(3)} ", end="")
				if '\033[32m' not in match.group(1):
					return True

		Halo(self.get_info_message("Executing tests")).info()
		has_errors, output = run_filter("./run.sh -lv", line_handler)
		if has_errors:
			show_errors_str(output, self.temp_dir, 20)
			outdir = (self.temp_dir / "outs").resolve()
			console.print(f"Output of the tests in: [purple]{outdir}[/purple]")
			console.print(f"Explanation of the files here: https://github.com/vfurmane/pipex-tester\n")
		return self.result(has_errors)
