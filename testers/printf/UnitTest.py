import logging

from halo import Halo
from testers.BaseExecutor import BaseExecutor

logger = logging.getLogger('pf-unit')


class UnitTest(BaseExecutor):

	name = 'printf-unit-test'
	folder = 'unit-test'
	git_url = 'https://github.com/alelievr/printf-unit-test'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		if not self.exec_bonus:
			return []
		with Halo(self.get_info_message("Compiling tests")) as spinner:
			self.call_make_command('', self.exec_bonus, True, spinner=spinner)
		output = self.run_tests("./run_test -e -r")
		print()
		return self.result("Total tested" not in output.splitlines()[-1])

	def check_errors(self, output):
		if output:
			raise Exception("Problem compiling tests")
