from dataclasses import dataclass
from typing import List


PART_1_FUNCTIONS = [
    "isalpha", "isdigit", "isalnum", "isascii", "isprint", "strlen", "memset", "bzero", "memcpy", "memmove", "strlcpy",
    "strlcat", "toupper", "tolower", "strchr", "strrchr", "strncmp", "memchr", "memcmp", "strnstr", "atoi", "calloc",
    "strdup"
]

PART_2_FUNCTIONS = [
    "substr", "strjoin", "strtrim", "split", "itoa", "strmapi", "striteri", "putchar_fd", "putstr_fd", "putendl_fd",
    "putnbr_fd"
]

BONUS_FUNCTIONS = [
    "lstnew", "lstadd_front", "lstsize", "lstlast", "lstadd_back", "lstdelone", "lstclear", "lstiter", "lstmap"
]


@dataclass
class TestRunInfo:
	project: str
	source_dir: str
	tests_dir: str
	temp_dir: str
	ex_to_execute: List[str]
	strict: bool
	has_bonus: bool


_saved_context = None


def set_contex(info: TestRunInfo):
	global _saved_context
	_saved_context = info


def get_context() -> TestRunInfo:
	return _saved_context


def set_bonus(value):
	_saved_context.has_bonus = value


def has_bonus():
	return _saved_context.has_bonus


def is_strict():
	return _saved_context.strict


def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3
