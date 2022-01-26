from testers.cpiscine.CommonTester import CommonTester
from utils.ExecutionContext import TestRunInfo


class C04Tester(CommonTester):

	name = "c04"

	def __init__(self, info: TestRunInfo):
		super().__init__(info)

	def ex00(self):
		self.exercise_files = ["ft_strlen.c"]
		self.test_files = ["main.c"]

	def ex01(self):
		self.exercise_files = ["ft_putstr.c"]
		self.test_files = ["main.c"]

	def ex02(self):
		self.exercise_files = ["ft_putnbr.c"]
		self.test_files = ["main.c"]

	def ex03(self):
		self.exercise_files = ["ft_atoi.c"]
		self.test_files = ["main.c"]

	def ex04(self):
		self.exercise_files = ["ft_putnbr_base.c"]
		self.test_files = ["main.c"]

	def ex05(self):
		self.exercise_files = ["ft_atoi_base.c"]
		self.test_files = ["main.c"]
