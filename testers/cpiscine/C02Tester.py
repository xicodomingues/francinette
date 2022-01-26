import re
from typing import Match

from testers.cpiscine.CommonTester import CommonTester, VeriOut
from utils.ExecutionContext import TestRunInfo


class C02Tester(CommonTester):

	name = "c02"

	def __init__(self, info: TestRunInfo):
		super().__init__(info)

	def ex00(self):
		self.exercise_files = ["ft_strcpy.c"]
		self.test_files = ["main.c"]

	def ex01(self):
		self.exercise_files = ["ft_strncpy.c"]
		self.test_files = ["main.c"]

	def ex02(self):
		self.exercise_files = ["ft_str_is_alpha.c"]
		self.test_files = ["main.c"]

	def ex03(self):
		self.exercise_files = ["ft_str_is_numeric.c"]
		self.test_files = ["main.c"]

	def ex04(self):
		self.exercise_files = ["ft_str_is_lowercase.c"]
		self.test_files = ["main.c"]

	def ex05(self):
		self.exercise_files = ["ft_str_is_uppercase.c"]
		self.test_files = ["main.c"]

	def ex06(self):
		self.exercise_files = ["ft_str_is_printable.c"]
		self.test_files = ["main.c"]

	def ex07(self):
		self.exercise_files = ["ft_strupcase.c"]
		self.test_files = ["main.c"]

	def ex08(self):
		self.exercise_files = ["ft_strlowcase.c"]
		self.test_files = ["main.c"]

	def ex09(self):
		self.exercise_files = ["ft_strcapitalize.c"]
		self.test_files = ["main.c"]

	def ex10(self):
		self.exercise_files = ["ft_strlcpy.c"]
		self.test_files = ["main.c"]

	def ex11(self):
		self.exercise_files = ["ft_putstr_non_printable.c"]
		self.test_files = ["main.c"]

	def ex12(self):
		self.exercise_files = ["ft_print_memory.c"]
		self.test_files = ["main.c"]

	@staticmethod
	def ex12_verification():

		def get_replacement(first_value):

			def replace(match: Match):
				return f"{(int(match.group(1), 16) - first_value):0>16x}"

			return replace

		def truncate(lines):
			return lines[:2] + ["..."] + lines[-2:]

		with open("out") as outfile, open("expected") as expfile:
			outlines = outfile.readlines()
			explines = expfile.readlines()

			if len(outlines) != len(explines):
				return VeriOut(
				    -1, f"The out and expected files "
				    f"do not have the same number of lines:"
				    f" {truncate(outlines)}, {truncate(outlines)}")

			first_value_out = int(outlines[1].split(":")[0], 16)
			first_value_exp = int(explines[1].split(":")[0], 16)
			for i in range(len(outlines)):
				line2 = re.sub(r"^([0-9a-f]{16}):", get_replacement(first_value_exp), explines[i])
				line1 = re.sub(r"^([0-9a-f]{16}):", get_replacement(first_value_out), outlines[i])
				if line1 != line2:
					return VeriOut(-2, f"These lines should be equal:\n{repr(line1)}\n{repr(line2)}")
			return VeriOut(0, "Ok")
