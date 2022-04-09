from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path
from typing import List

from rich.console import Console

console = Console()


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


def get_timeout():
	return int(_saved_context.args.timeout)


def set_timeout(timeout: int):
	_saved_context.args.timeout = timeout
