from dataclasses import dataclass
from typing import List


@dataclass
class TestRunInfo:
	project: str
	source_dir: str
	tests_dir: str
	temp_dir: str
	ex_to_execute: List[str]
	strict: bool


_saved_context = None


def set_contex(info: TestRunInfo):
	global _saved_context
	_saved_context = info


def get_context():
	return _saved_context


def is_strict():
	return _saved_context.strict