

from testers.libft.BaseExecutor import BaseExecutor


class ExecuteFsoares(BaseExecutor):

	def __init__(self, tests_dir, temp_dir, to_execute) -> None:
		self.temp_dir = temp_dir
		self.to_execute = to_execute
		self.tests_dir = tests_dir
		self.folder = "fsoares"

	def execute(self):
		self.compile_test()
		pass

	def compile_test(self):
		pass
