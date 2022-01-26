from testers.cpiscine.CommonTester import CommonTester
from utils.ExecutionContext import TestRunInfo


class C01Tester(CommonTester):

	name = "c01"

	def __init__(self, info: TestRunInfo):
		super().__init__(info)

	def ex00(self):
		self.exercise_files = ["ft_ft.c"]
		self.test_files = ["main.c"]

	def ex01(self):
		self.exercise_files = ["ft_ultimate_ft.c"]
		self.test_files = ["main.c"]

	def ex02(self):
		self.exercise_files = ["ft_swap.c"]
		self.test_files = ["main.c"]

	def ex03(self):
		self.exercise_files = ["ft_div_mod.c"]
		self.test_files = ["main.c"]

	def ex04(self):
		self.exercise_files = ["ft_ultimate_div_mod.c"]
		self.test_files = ["main.c"]

	def ex05(self):
		self.exercise_files = ["ft_putstr.c"]
		self.test_files = ["main.c"]

	def ex06(self):
		self.exercise_files = ["ft_strlen.c"]
		self.test_files = ["main.c"]

	def ex07(self):
		self.exercise_files = ["ft_rev_int_tab.c"]
		self.test_files = ["main.c"]

	def ex08(self):
		self.exercise_files = ["ft_sort_int_tab.c"]
		self.test_files = ["main.c"]
