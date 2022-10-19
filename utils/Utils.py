import logging
import os
import re
from pathlib import Path
import shutil
import signal
import subprocess
import sys

from rich import print
from rich.text import Text

from utils.TerminalColors import TC
from utils.TraceToLine import TraceToLine, open_utf8

FILE_SHOW_LINES = 50
REPO_URL = "https://raw.githubusercontent.com/xicodomingues/francinette/master/"

logger = logging.getLogger("utils")


def show_banner(project):
	columns = shutil.get_terminal_size((80, 23)).columns
	#print(columns)
	message = f"[blue]Welcome to [b][purple]Francinette[/b][blue], a 42 tester framework!"
	submessage = f"{project}"
	project_message = f"[b][yellow]{project}[/b][cyan]"
	size = 30 - len(submessage)
	project_message = " " * (size - (size // 2)) + project_message + " " * (size // 2)
	print(f"[cyan]╔══════════════════════════════════════════════════════════════════════════════╗")
	print(f"[cyan]║                {message}                [cyan]║")
	print(f"[cyan]╚═══════════════════════╦══════════════════════════════╦═══════════════════════╝")
	print(f"[cyan]                        ║{project_message}║")
	print(f"[cyan]                        ╚══════════════════════════════╝[/cyan]")


def intersection(lst1, lst2):
	lst3 = [value for value in lst1 if value in lst2]
	return lst3


ansi_columns = re.compile(r'\x1B(?:\[[0-?]*G)')
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def remove_ansi_colors(text):
	return ansi_escape.sub('', ansi_columns.sub(' ', text))


def open_ascii(file, mode='r'):
	return open(file, mode, encoding='ascii', errors="backslashreplace")


def decode_ascii(bytes):
	return bytes.decode('ascii', errors="backslashreplace")


def show_errors_file(temp_dir: Path, errors_color, errors_log, n_lines=FILE_SHOW_LINES):
	trace_to_line = TraceToLine(temp_dir, errors_color)
	lines = trace_to_line.parse_stack_traces()
	lines = list(filter(lambda x: x != '', lines))

	print(f"[b red]Errors found[/b red]:")
	[print(Text.from_ansi(line)) for line in lines[:n_lines]]
	if len(lines) > n_lines:
		dest = (temp_dir / errors_log).resolve()
		with open_utf8(dest, "w") as log:
			log.writelines([remove_ansi_colors(line) for line in lines])
		print(f"...\n\nFile too large. To see full report open: [purple]{dest}[/purple]")
	print()


def show_errors_str(errors: str, temp_dir: Path, n_lines=FILE_SHOW_LINES):
	with open_utf8('error_color.log', 'w') as f:
		f.write(errors)
	show_errors_file(temp_dir, "error_color.log", "errors.log", n_lines)


def save_err_file(errors: str, temp_dir: Path):
	with open_utf8('execution.log', 'w') as f:
		f.writelines([remove_ansi_colors(line) for line in errors.splitlines(True)])
	dest = (temp_dir / 'execution.log').resolve()
	print(f"To see the execution log open: [purple]{dest}[/purple]");


def is_makefile_project(current_path, project_name, project_class):
	make_path = current_path / "Makefile"
	name_matcher = re.compile(rf"^\s*NAME\s*:?=\s*{project_name}\s*$")
	logger.info(f"Makefile path: {make_path.resolve()}")
	if not make_path.exists():
		return False
	with open(make_path, "r") as mk:
		for line in mk.readlines():
			if name_matcher.match(line):
				return project_class

	return False


def is_linux():
	return sys.platform.startswith("linux")


def is_mac():
	return not is_linux()


def escape_str(string):
	temp = re.sub(r"\\(?!x)", r"\\\\", string)
	return temp.replace('"', r'\"') \
		.replace('\t', r'\t') \
		.replace('\n', r'\n') \
		.replace('\f', r'\f') \
		.replace('\v', r'\v') \
		.replace('\r', r'\r')


def run_filter(command, line_handler):
	"""

	Args:
		command (str): The command to be executed
		line_handler (fn): The function that will be called to handle each line.
		This function should received one parameter, the line, and return a boolean
		indicating if there is any error with the result of the line being parsed

	Returns:
		(bool, str): A tuple with if there was errors and the complete output of the command
	"""
	proc = subprocess.Popen(command,
		                        shell="True",
		                        errors="backslashreplace",
		                        stdout=subprocess.PIPE)
	output = ""
	has_errors = False
	while True:
		line = proc.stdout.readline()
		if not line:
			break
		has_errors = line_handler(line) or has_errors
		output += line
	print('\n')
	return has_errors, output
