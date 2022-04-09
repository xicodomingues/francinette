from testers.BaseTester import BaseTester
from testers.pipex.Fsoares import Fsoares
from testers.pipex.Medic import Medic
from testers.pipex.Vfurname import Vfurname
from utils.ExecutionContext import TestRunInfo
from utils.Utils import is_makefile_project


class Pipex(BaseTester):

	name = "pipex"
	my_tester = Fsoares
	testers = [Vfurname, Medic, Fsoares]
	timeout = 1

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		self.execute_testers()
		pass

	@staticmethod
	def is_project(current_path):
		return is_makefile_project(current_path, "pipex", Pipex)
