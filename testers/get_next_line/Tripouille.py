import logging
import os

import pexpect
from halo import Halo
from testers.get_next_line.BaseExecutor import BaseExecutor
from utils.TerminalColors import TC

logger = logging.getLogger('gnl-trip')


class Tripouille(BaseExecutor):

	name = 'gnlTester'
	folder = 'gnlTester'
	git_url = 'https://github.com/Tripouille/gnlTester'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		output = self.run_tests("make m")
		return []
