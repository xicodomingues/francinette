import logging
import re
from testers.BaseTester import BaseTester
from testers.minitalk.Fsoares import Fsoares
from utils.ExecutionContext import TestRunInfo
from utils.Utils import is_makefile_project

logger = logging.getLogger('minitalk')

class Minitalk(BaseTester):

	name = "minitalk"
	my_tester = Fsoares
	testers = [Fsoares]
	timeout = 20

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		self.execute_testers()
		pass

	@staticmethod
	def is_project(current_path):
		if (Minitalk.makefile_contains(current_path, "server")
				and Minitalk.makefile_contains(current_path, "client")):
			return Minitalk
		return False

	@staticmethod
	def makefile_contains(current_path, name):
		make_path = current_path / "Makefile"
		name_matcher = re.compile(fr".*\b({name})(?![\w\.]).*")
		logger.info(f"Makefile path: {make_path.resolve()}")
		if not make_path.exists():
			return False
		with open(make_path, "r") as mk:
			for line in mk.readlines():
				if name_matcher.match(line):
					return True
		return False
