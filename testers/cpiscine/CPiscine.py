import logging
import os

from testers.BaseTester import BaseTester
from testers.cpiscine.C00Tester import C00Tester
from testers.cpiscine.C01Tester import C01Tester
from testers.cpiscine.C02Tester import C02Tester
from testers.cpiscine.C03Tester import C03Tester
from testers.cpiscine.C04Tester import C04Tester
from testers.cpiscine.C05Tester import C05Tester
from utils.ExecutionContext import TestRunInfo

logger = logging.getLogger('c selector')


def has_file(ex_path, file):
	path = os.path.join(ex_path, file)
	logger.info(f"Testing path: {path}")
	return os.path.exists(path)


class CPiscine(BaseTester):

	def __init__(self, info: TestRunInfo) -> None:
		super().__init__(info)

	@staticmethod
	def is_project(current_path):
		ex_path = (current_path / "ex00").resolve()
		logger.info(f"Testing path: {ex_path}")
		if os.path.exists(ex_path):
			if has_file(ex_path, "ft_putchar.c"):
				return C00Tester
			if has_file(ex_path, "ft_ft.c"):
				return C01Tester
			if has_file(ex_path, "ft_strcpy.c"):
				return C02Tester
			if has_file(ex_path, "ft_strcmp.c"):
				return C03Tester
			if has_file(ex_path, "ft_strlen.c"):
				return C04Tester
			if has_file(ex_path, "ft_iterative_factorial.c"):
				return C05Tester
		return False
