import logging
import re

from testers.BaseTester import BaseTester
from testers.minitalk.Fsoares import Fsoares
from utils.ExecutionContext import TestRunInfo
from utils.Utils import is_makefile_project


test_line_regex = re.compile("^([^#]+)# (\d+):.*\[(\w+)\]$")

class Minishell(BaseTester):

	name = 'minishell'
	folder = '42_minishell_tester'
	git_url = 'https://github.com/zstenger93/42_minishell_tester'


	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):