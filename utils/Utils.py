import re
from utils.TerminalColors import TC


def show_banner(project):
	message = f"Welcome to {TC.B_PURPLE}Francinette{TC.B_BLUE}, a 42 tester framework!"
	submessage = f"{project}"
	project_message = f"{TC.B_YELLOW}{project}{TC.B_BLUE}"
	size = 30 - len(submessage)
	project_message = " " * (size - (size // 2)) + project_message + " " * (size // 2)
	print(f"{TC.B_BLUE}╔══════════════════════════════════════════════════════════════════════════════╗")
	print(f"{TC.B_BLUE}║                {message}                ║")
	print(f"{TC.B_BLUE}╚═══════════════════════╦══════════════════════════════╦═══════════════════════╝")
	print(f"{TC.B_BLUE}                        ║{project_message}║")
	print(f"{TC.B_BLUE}                        ╚══════════════════════════════╝{TC.NC}")


ansi_columns = re.compile(r'\x1B(?:\[[0-?]*G)')
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def remove_ansi_colors(text):
	return ansi_escape.sub('', ansi_columns.sub(' ', text))

def open_ascii(file, mode='r'):
	return open(file, mode, encoding='ascii', errors="backslashreplace")