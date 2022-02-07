import logging
from pathlib import Path
from testers.BaseTester import BaseTester
from testers.get_next_line.Fsoares import Fsoares

from testers.get_next_line.Tripouille import Tripouille
from utils.ExecutionContext import TestRunInfo, is_strict
from utils.Utils import show_banner

logger = logging.getLogger("gnl")


class GetNextLineTester(BaseTester):

	name = "get_next_line"
	testers = [Tripouille, Fsoares]

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		self.execute_testers()
		pass

	@staticmethod
	def is_project(current_path):
		file_path = current_path / 'get_next_line.c'
		logger.info(f"Testing: {file_path}")
		if not file_path.exists():
			return False
		return GetNextLineTester

	def test_selector(self):
		result = super().test_selector()
		if is_strict() and Fsoares in result:
			return [Fsoares]
		return result
