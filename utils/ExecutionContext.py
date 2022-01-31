from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class TestRunInfo:
	source_dir: Path 	# location of the code to test
	base_dir: Path		# location of francinette
	ex_to_execute: List[str]
	args: Namespace
	has_bonus: bool = False


_saved_context = None


def set_contex(info: TestRunInfo):
	global _saved_context
	_saved_context = info


def get_context() -> TestRunInfo:
	return _saved_context


def set_bonus(value):
	_saved_context.has_bonus = value


def has_bonus() -> bool:
	return _saved_context.has_bonus


def is_strict():
	return _saved_context.args.strict


def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3
