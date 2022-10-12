import logging
import re

from utils.TerminalColors import TC

logger = logging.getLogger()
ansi_columns = re.compile(r'\x1B(?:\[[0-?]*G)')
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

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


def remove_ansi_colors(text):
	return ansi_escape.sub('', ansi_columns.sub(' ', text))
