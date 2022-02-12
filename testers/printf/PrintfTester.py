

import logging
from testers.BaseTester import BaseTester
from testers.printf.Fsoares import Fsoares
from utils.ExecutionContext import TestRunInfo, is_strict, set_bonus
from utils.Utils import is_makefile_project

logger = logging.getLogger('printf')

class PrintfTester(BaseTester):

	name = "printf"
	my_tester = Fsoares
	testers = [Fsoares]

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		self.execute_testers()
		pass

	@staticmethod
	def is_project(current_path):
		return is_makefile_project(current_path, "libftprintf.a", PrintfTester)