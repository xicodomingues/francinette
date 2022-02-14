import logging
import re
from pathlib import Path

from utils.TerminalColors import TC

FILE_SHOW_LINES = 50

logger = logging.getLogger("utils")


def show_banner(project):
	message = f"{TC.BLUE}Welcome to {TC.B_PURPLE}Francinette{TC.BLUE}, a 42 tester framework!"
	submessage = f"{project}"
	project_message = f"{TC.B_YELLOW}{project}{TC.CYAN}"
	size = 30 - len(submessage)
	project_message = " " * (size - (size // 2)) + project_message + " " * (size // 2)
	print(f"{TC.CYAN}╔══════════════════════════════════════════════════════════════════════════════╗")
	print(f"{TC.CYAN}║                {message}                {TC.CYAN}║")
	print(f"{TC.CYAN}╚═══════════════════════╦══════════════════════════════╦═══════════════════════╝")
	print(f"{TC.CYAN}                        ║{project_message}║")
	print(f"{TC.CYAN}                        ╚══════════════════════════════╝{TC.NC}")


def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3


ansi_columns = re.compile(r'\x1B(?:\[[0-?]*G)')
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def remove_ansi_colors(text):
	return ansi_escape.sub('', ansi_columns.sub(' ', text))


def open_ascii(file, mode='r'):
	return open(file, mode, encoding='ascii', errors="backslashreplace")


def show_errors_file(errors_color_path: Path, errors_log_path: Path):
	with open_ascii(errors_color_path) as f:
		lines = f.readlines()
	print(f"{TC.B_RED}Errors found{TC.NC}:")
	[print(line, end='') for line in lines[:50]]
	if len(lines) > FILE_SHOW_LINES:
		dest = errors_log_path.resolve()
		with open_ascii(errors_color_path, "r") as orig, open(dest, "w") as log:
			log.write(remove_ansi_colors(orig.read()))
		print(f"...\n\nFile too large. To see full report open: {TC.PURPLE}{dest}{TC.NC}")
	print()


def is_makefile_project(current_path, project_name, project_class):
	make_path = current_path / "Makefile"
	logger.info(f"Makefile path: {make_path.resolve()}")
	if not make_path.exists():
		return False
	with open(make_path, "r") as mk:
		if project_name in mk.read():
			return project_class
		else:
			return False
