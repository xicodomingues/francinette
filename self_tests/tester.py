import difflib
import os
import re
from dataclasses import dataclass
import sys
from unittest import result

import pexpect
from utils.ExecutionContext import console

ansi_columns = re.compile(r'\x1B(?:\[[0-?]*G)')
ansi_colors = re.compile(r'\x1B(?:\[\??[\d;]+(?:m|l|h))')
pointer_addr = re.compile(r'0x[0-9a-f]{8,16}')
sanitizer_pid = re.compile(r'==(\d+)==')
pid_clock = re.compile(r'\d+ Alarm clock')

TESTS = [
    # (project, path, [(output_file, paco_params)], [files_to_check])
    #('libft', 'libft/ok', [("expected", ""), ("mandatory", "-m"), ("bonus", "-b"), ("strict", "--strict"),
    #                       ("some", "memset split lstnew")], []),
	('libft', 'libft/errors', [("errors", ''), ('norm', 'lstsize'),
	 ("sanitizer", "substr"), ("leaks", "strjoin"), ("null_check", "split lstmap --strict"), ("timeout", "lstlast")
	 ], ["war-machine/errors.log", "alelievr/result.log", "fsoares/error.log"])
]


def clean_output(text):
	text = ansi_colors.sub('', text).replace('\0', '')
	text = ansi_columns.sub(' ', text)
	text = pointer_addr.sub("0x_address", text)
	text = pid_clock.sub('<pid> Alarm clock', text)
	if sanitizer_pid.search(text):
		pids = set(sanitizer_pid.findall(text))
		for pid in pids:
			text = re.sub(r'\b' + re.escape(pid) + r'\b', "<pid>", text)
	lines = text.splitlines()
	for i, line in enumerate(lines):
		if '\x1B[K' in line:
			lines[i - 1] = ""
			lines[i] = line.replace('\x1B[K', '')
	text = "\n".join([line.rstrip() for line in lines if line != ""])
	return text


def color_diff(diff):
	for line in diff:
		if line.startswith('+'):
			yield f'[green]{line}[/green]'
		elif line.startswith('-'):
			yield f'[red]{line}[/red]'
		elif line.startswith('^'):
			yield f'[blue]{line}[/blue]'
		else:
			yield line


def compare_to_expected(test_path, test_name, actual):
	with open(f"{test_path}/{test_name}") as f:
		expected_lines = f.readlines()
	actual_lines = actual.splitlines(True)

	diff = difflib.unified_diff(expected_lines, actual_lines, fromfile="expected", tofile="actual")
	res = "".join(color_diff(diff));
	if res:
		console.print(res)


def add_files(base_path, project, files):
	result = ""
	for file in files:
		file = base_path.joinpath("temp", project, file)
		if file.exists():
			result += f"\n\n=====> File {file} contents:\n"
			with open(file, errors="backslashreplace") as f:
				result += f.read()
	result = clean_output(result)
	return result


def execute_test(base_path, project, test_path, test_params, files, save_output=False):
	base_integration_tests = base_path.joinpath("self_tests").resolve()
	os.chdir(base_integration_tests)

	with console.status(
	    f"[b white]Testing[/b white]: {test_path}: {test_params[0]} with options: '{test_params[1]}'") as status:
		path = base_path.joinpath(f"self_tests/{test_path}/{project}").resolve()
		os.chdir(path)

		exec = base_path.joinpath(f"tester.sh").resolve()
		proc = pexpect.run(str(exec) + " " + test_params[1], encoding='utf-8', timeout=None)

	actual = clean_output(proc)
	actual += add_files(base_path, project, files)
	#compate_files(f'{base_integration_tests}/{test}/expected.output', actual)

	os.chdir(base_integration_tests)
	if not save_output:
		compare_to_expected(test_path, test_params[0], actual)

	if save_output:
		with open(base_path.joinpath(f"self_tests/{test_path}/{test_params[0]}"), 'w') as out:
			out.write(actual)

	print(f"{test_path}: {test_params[0]} with options: '{test_params[1]}' done!")


def integration_test(base_path):
	for test in TESTS:
		for test_config in test[2]:
			execute_test(base_path, test[0], test[1], test_config, test[3], True)