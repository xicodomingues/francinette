import logging
from pathlib import Path
from testers.BaseTester import BaseTester
from testers.get_next_line.Fsoares import Fsoares

from testers.get_next_line.Tripouille import Tripouille
from utils.ExecutionContext import TestRunInfo, has_bonus, is_strict, set_bonus
from utils.Utils import show_banner

logger = logging.getLogger("gnl")


class GetNextLine(BaseTester):

	name = "get_next_line"
	my_tester = Fsoares
	testers = [Tripouille, Fsoares]
	timeout = 10

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)
		if (info.source_dir / "get_next_line_bonus.c").exists() \
				and not info.args.mandatory:
			logger.info("Has bonus")
			set_bonus(True)
		self.execute_testers()

	@staticmethod
	def is_project(current_path):
		file_path = current_path / 'get_next_line.c'
		logger.info(f"Testing: {file_path}")
		if not file_path.exists():
			return False
		return GetNextLine
