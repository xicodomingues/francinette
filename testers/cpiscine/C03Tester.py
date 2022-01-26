from testers.cpiscine.CommonTester import CommonTester
from utils.ExecutionContext import TestRunInfo


class C03Tester(CommonTester):

	name = "c03"

	def __init__(self, info: TestRunInfo):
		super().__init__(info)

	def ex00(self):
		self.exercise_files = ["ft_strcmp.c"]
		self.test_files = ["main.c"]

	def ex01(self):
		self.exercise_files = ["ft_strncmp.c"]
		self.test_files = ["main.c"]

	def ex02(self):
		self.exercise_files = ["ft_strcat.c"]
		self.test_files = ["main.c"]

	def ex03(self):
		self.exercise_files = ["ft_strncat.c"]
		self.test_files = ["main.c"]

	def ex04(self):
		self.exercise_files = ["ft_strstr.c"]
		self.test_files = ["main.c"]

	def ex05(self):
		self.exercise_files = ["ft_strlcat.c"]
		self.test_files = ["main.c"]
