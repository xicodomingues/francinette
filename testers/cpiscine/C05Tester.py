from testers.cpiscine.CommonTester import CommonTester
from utils.ExecutionContext import TestRunInfo


class C05Tester(CommonTester):

	name = "c05"

	def __init__(self, info: TestRunInfo):
		super().__init__(info)

	def ex00(self):
		self.exercise_files = ["ft_iterative_factorial.c"]
		self.test_files = ["main.c"]

	def ex01(self):
		self.exercise_files = ["ft_recursive_factorial.c"]
		self.test_files = ["main.c"]

	def ex02(self):
		self.exercise_files = ["ft_iterative_power.c"]
		self.test_files = ["main.c"]

	def ex03(self):
		self.exercise_files = ["ft_recursive_power.c"]
		self.test_files = ["main.c"]

	def ex04(self):
		self.exercise_files = ["ft_fibonacci.c"]
		self.test_files = ["main.c"]

	def ex05(self):
		self.exercise_files = ["ft_sqrt.c"]
		self.test_files = ["main.c"]

	def ex06(self):
		self.exercise_files = ["ft_is_prime.c"]
		self.test_files = ["main.c"]

	def ex07(self):
		self.exercise_files = ["ft_find_next_prime.c"]
		self.test_files = ["main.c"]

	def ex08(self):
		self.exercise_files = ["ft_ten_queens_puzzle.c"]
		self.test_files = ["main.c"]
