import abc
from utils.ExecutionContext import TestRunInfo
from utils.TerminalColors import TC


class BaseTester:

	name = "base"
	testers = []

	def __init__(self, info: TestRunInfo) -> None:
		self.info = info
		self.temp_dir = info.base_dir / "temp" / self.name
		self.tests_dir = info.base_dir / "tests" / self.name

	@staticmethod
	@abc.abstractmethod
	def is_project(current_dir):
		pass

	def test_selector(self, info: TestRunInfo):
		selected_testers = info.args.testers
		if (selected_testers == None):
			return self.testers
		if (selected_testers == []):
			print(f"Please select one or more of the available testers:")
			for i, tester in enumerate(self.testers):
				print(f"{TC.B_BLUE}    {i + 1}) {TC.B_WHITE}{tester.name}{TC.NC} ({tester.git_url})")
			print(f"You can pass the numbers as arguments to {TC.B_WHITE}--testers{TC.NC} to not see this prompt")
			testers = [char for char in input()]
		testers = [test for test in ''.join(testers) if test != ' ']
		return [testers[int(i) - 1] for i in testers]

