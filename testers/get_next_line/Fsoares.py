
from asyncio import subprocess
import logging
import os
from pipes import quote

import pexpect
from testers.get_next_line.BaseExecutor import BaseExecutor

logger = logging.getLogger("fsoares")

class Fsoares(BaseExecutor):

	name = 'fsoares'
	folder = 'fsoares'
	git_url = 'my own tests'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		raise Exception("Not implemented yet")
