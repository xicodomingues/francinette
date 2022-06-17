import logging

from testers.BaseTester import BaseTester
from testers.printf.Cacharle import Cacharle
from testers.printf.Fsoares import Fsoares
from testers.printf.Tripouille import Tripouille
from testers.printf.UnitTest import UnitTest
from utils.ExecutionContext import TestRunInfo
from utils.Utils import is_makefile_project

logger = logging.getLogger('printf')


class Printf(BaseTester):

	name = "printf"
	my_tester = Fsoares
	testers = [Tripouille, UnitTest, Cacharle, Fsoares]
	timeout = 2

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		self.execute_testers()
		pass

	@staticmethod
	def is_project(current_path):
		return is_makefile_project(current_path, "libftprintf.a", Printf)
