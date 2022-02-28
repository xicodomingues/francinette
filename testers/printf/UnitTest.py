import logging

from halo import Halo
from testers.BaseExecutor import BaseExecutor

logger = logging.getLogger('pf-trip')


#add later
# https://github.com/gavinfielder/pft
# https://github.com/Mazoise/42TESTERS-PRINTF
# https://github.com/charMstr/printf_lover_v2
# https://github.com/cacharle/ft_printf_test
class UnitTest(BaseExecutor):

	name = 'printf-unit-test'
	folder = 'unit-test'
	git_url = 'https://github.com/alelievr/printf-unit-test'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		with Halo(self.get_info_message("Compiling tests")) as spinner:
			self.call_make_command('', self.exec_bonus, True, spinner=spinner)
		output = self.run_tests("./run_test -e -r")
		print()
		if "Total tested" not in output.splitlines()[-1]:
			return [self.name]
		else:
			return []

	def check_errors(self, output):
		if output:
			raise Exception("Problem compiling tests")
