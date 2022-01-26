from testers.cpiscine.CommonTester import CommonTester
from utils.ExecutionContext import TestRunInfo


class C00Tester(CommonTester):

	name = "c00"

	def __init__(self, info: TestRunInfo):
		super().__init__(info)

	def ex00(self):
		self.exercise_files = ["ft_putchar.c"]
		self.test_files = ["main.c"]

	def ex01(self):
		self.exercise_files = ["ft_print_alphabet.c"]
		self.test_files = ["main.c"]

	def ex02(self):
		self.exercise_files = ["ft_print_reverse_alphabet.c"]
		self.test_files = ["main.c"]

	def ex03(self):
		self.exercise_files = ["ft_print_numbers.c"]
		self.test_files = ["main.c"]

	def ex04(self):
		self.exercise_files = ["ft_is_negative.c"]
		self.test_files = ["main.c"]

	def ex05(self):
		self.exercise_files = ["ft_print_comb.c"]
		self.test_files = ["main.c"]

	def ex06(self):
		self.exercise_files = ["ft_print_comb2.c"]
		self.test_files = ["main.c"]

	def ex07(self):
		self.exercise_files = ["ft_putnbr.c"]
		self.test_files = ["main.c"]

	def ex08(self):
		self.exercise_files = ["ft_print_combn.c"]
		self.test_files = ["main.c"]
