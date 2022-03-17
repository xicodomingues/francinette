import logging
import re
from typing import Set

from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_timeout, has_bonus, is_strict
from utils.TerminalColors import TC
from utils.TraceToLine import TraceToLine
from utils.Utils import show_errors_file

logger = logging.getLogger("pipex-fso")


class Fsoares(BaseExecutor):

	name = 'fsoares'
	folder = 'fsoares'
	git_url = 'my own tests'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		return []