import logging
from pathlib import Path

from testers.get_next_line.TripouilleTester import Tripouille
from utils.ExecutionContext import TestRunInfo
from utils.Utils import show_banner

logger = logging.getLogger("gnl")


class GetNextLineTester():

	testers = [Tripouille]

	def __init__(self, info: TestRunInfo) -> None:
		show_banner("get_next_line")
		self.info = info
		pass

	@staticmethod
	def is_project(current_dir):
		file_path = Path('get_next_line.c')
		logger.info(f"Testing: {file_path}")
		if not file_path.exists():
			return False
		return GetNextLineTester
