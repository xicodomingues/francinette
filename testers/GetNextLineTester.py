
from testers.CommonTester import show_banner
from utils.ExecutionContext import TestRunInfo


class GetNextLineTester():

	def __init__(self, info: TestRunInfo) -> None:
		show_banner("get_next_line")
		self.info = info;
		pass;

	# strjoin calls the others in alever