

from testers.BaseExecutor import BaseExecutor


class Fsoares(BaseExecutor):

	name = "fsoares"
	folder = 'fsoares'
	git_url = 'my own tests'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		return []

"""
Test ideas:
	- %%c %%%c %c%c %<valid_flag>c
	- width: 0, 1 - 10, 10000
	
"""