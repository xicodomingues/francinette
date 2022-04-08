import logging

from halo import Halo
from testers.BaseExecutor import BaseExecutor

logger = logging.getLogger('pf-charle')


class Cacharle(BaseExecutor):

	name = 'ft_printf_test'
	folder = 'ft_printf_test'
	git_url = 'https://github.com/cacharle/ft_printf_test'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		if not self.exec_bonus:
			return []
		with Halo(self.get_info_message("Compiling tests")) as spinner:
			self.call_make_command('all', self.exec_bonus, True, spinner=spinner)

		output = self.run_tests("make quiet")
		return self.result(not output.splitlines()[-2].startswith('====='))
