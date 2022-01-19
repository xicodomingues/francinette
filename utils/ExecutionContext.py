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
	timeout: int


_saved_context = None


def set_contex(info: TestRunInfo):
	global _saved_context
	_saved_context = info


def get_context() -> TestRunInfo:
	return _saved_context


def get_timeout_script() -> str:
	if _saved_context.timeout == '0s':
		return ""
	return f"$HOME/francinette/utils/timeout.sh {_saved_context.timeout} "


def is_strict():
	return _saved_context.strict