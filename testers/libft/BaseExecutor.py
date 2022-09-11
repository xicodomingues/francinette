import logging
import re

from utils.TerminalColors import TC

logger = logging.getLogger()
ansi_columns = re.compile(r'\x1B(?:\[[0-?]*G)')
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

PART_1_FUNCTIONS = [
    "atoi",
    "bzero",
    "calloc",
    "isalnum",
    "isalpha",
    "isascii",
    "isdigit",
    "isprint",
    "memchr",
    "memcmp",
    "memcpy",
    "memmove",
    "memset",
    "strchr",
    "strdup"
    "strlcat",
    "strlcpy",
    "strlen",
    "strncmp",
    "strnstr",
    "strrchr",
    "tolower",
    "toupper",
]

PART_2_FUNCTIONS = [
    "itoa",
    "putchar_fd",
    "putendl_fd",
    "putnbr_fd"
    "putstr_fd",
    "split",
    "striteri",
    "strjoin",
    "strmapi",
    "strtrim",
    "substr",
]

BONUS_FUNCTIONS = [
    "lstadd_back",
    "lstadd_front",
    "lstclear",
    "lstdelone",
    "lstiter",
    "lstlast",
    "lstmap"
    "lstnew",
    "lstsize",
]


def remove_ansi_colors(text):
    return ansi_escape.sub('', ansi_columns.sub(' ', text))
