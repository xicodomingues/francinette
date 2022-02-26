import logging
import re

from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_timeout
from utils.TerminalColors import TC
from utils.Utils import remove_ansi_colors

logger = logging.getLogger('pf-trip')


#this one is for strict based implementations
#add later
# https://github.com/gavinfielder/pft
# https://github.com/Mazoise/42TESTERS-PRINTF
# https://github.com/charMstr/printf_lover_v2
# https://github.com/cacharle/ft_printf_test
class UnitTest(BaseExecutor):

	name = 'printf-unit-test'
	folder = 'unit-test'
	git_url = 'https://github.com/alelievr/printf-unit-test'
	test_regex = re.compile(r"(\d+|LEAKS)\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		print("ajdlkgjsdglgsl")
		return []
