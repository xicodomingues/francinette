import abc
from utils.ExecutionContext import TestRunInfo


class BaseTester:

	name = "base"

	def __init__(self, info: TestRunInfo) -> None:
		self.info = info
		self.temp_dir = info.base_dir / "temp" / self.name
		self.tests_dir = info.base_dir / "tests" / self.name

	@staticmethod
	@abc.abstractmethod
	def is_project(current_dir):
		pass