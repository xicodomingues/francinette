import logging
import os
import re
import shutil
import time
from dataclasses import dataclass
from pipes import quote
from subprocess import CompletedProcess, TimeoutExpired, run
from typing import List

from halo import Halo
import pexpect
from rich import box
from rich.table import Table
from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import console, get_timeout
from utils.LeaksCheck import LeakException, has_leaks
from utils.TraceToLine import open_ascii
from utils.Utils import escape_str, show_errors_str

logger = logging.getLogger("pipex-fso")


@dataclass
class TestCase:
	id: int
	params: List[str]
	description: str
	path: str = os.environ['PATH']
	input: str = None


@dataclass
class ProcResult:
	stdout: str
	stderr: str
	returncode: int


def run_bash(command, test, timeout=None):
	my_env = os.environ.copy()
	if test.path != None:
		my_env["PATH"] = test.path
	if test.path == None:
		my_env.pop("PATH")
	if timeout is None:
		timeout = get_timeout()
	_input = None
	if test.params[0] == "here_doc":
		if command.startswith("./pipex"):
			_input = test.input
		else:
			heredoc = f"#!/bin/bash\n\n{command}\n{test.input}\n"
			open('heredoc.sh', 'w').write(heredoc)
			command = "./heredoc.sh"

	try:
		return run(command,
				capture_output=True,
				shell="True",
				encoding="ascii",
				errors="backslashreplace",
				env=my_env,
				timeout=timeout,
				input=_input)
	except Exception as ex:
		logger.error(ex)


def get_commands(test: TestCase):
	infile, cmd1, *cmds, outfile = test.params
	if infile != "here_doc":
		cms = " | ".join(cmds)
		native = f"< {infile} {cmd1} | {cms} > {outfile}"
		cms = " ".join(quote(cmd) for cmd in cmds)
		pipex = f'./pipex {infile} {quote(cmd1)} {cms} {outfile}'

	else:
		heredoc, limiter, cmd1, cmd2, outfile = test.params
		native = f"{cmd1} << {limiter} | {cmd2} >> {outfile}"
		pipex = f'./pipex {heredoc} {limiter} {quote(cmd1)} {quote(cmd2)} {outfile}'

	logger.info(f'command: native: "{native}", pipex: "{pipex}"')
	path = test.path
	if path == os.environ['PATH']:
		path = 'default'
	return (native, pipex, path)


class Fsoares(BaseExecutor):

	name = 'fsoares'
	folder = 'fsoares'
	git_url = 'my own tests'

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)
		# macOS: suppress inconsequential but intrusive
		# debug messages printed by Apple's libmalloc
		os.environ['MallocNanoZone'] = '0'

	def execute(self):
		Halo(self.get_info_message("Executing tests")).info()
		res_m, res_b = [], []
		if self.exec_mandatory:
			self.execute_in_project_dir("make fclean all")
			res_m = self.execute_batch()
			res_m += self.test_sleep()
			res_m += self.test_leak(False)
			console.print("\n", style="default")

		if self.exec_bonus:
			console.print("[Bonus]", style="purple")
			self.execute_in_project_dir("make fclean bonus")
			res_b = self.execute_batch(True)
			res_b += self.test_sleep(True)
			res_b += self.test_leak(True)
			console.print("\n", style="default")

		has_errors = self.show_test_results(res_m + res_b)
		return self.result(has_errors)

	def test_sleep(self, is_bonus=False):
		if not is_bonus:
			tests = [
			    TestCase(32, ['infile.txt', "sleep 1", 'sleep 3', 'outfile.txt'], 'Should sleep for 3 seconds'),
			    TestCase(33, ['infile.txt', "sleep 3", 'sleep 1', 'outfile.txt'], 'Should sleep for 3 seconds'),
			    TestCase(34, ['infile.txt', "sleep 3", 'sleep 3', 'outfile.txt'], 'Should sleep for 3 seconds')
			]
		else:
			tests = [
			    TestCase(40, ['infile.txt', "sleep 1", 'sleep 3', 'sleep 2', 'sleep 1', 'outfile.txt'],
			             'Should sleep for 3 seconds'),
			    TestCase(41, ['infile.txt', "sleep 1", 'sleep 3', 'sleep 2', 'sleep 3', 'outfile.txt'],
			             'Should sleep for 3 seconds'),
			    TestCase(42, ['here_doc', '"sleep 10"', "sleep 3", "sleep 1", 'outfile.txt'],
			             'Should sleep for 3 seconds',
			             input="EOF\nsleep 10\n")
			]
		return [self.__test_sleep(test) for test in tests]

	def test_leak(self, is_bonus=False):
		try:
			output = ""
			if not is_bonus:
				output = has_leaks("./pipex infile.txt cat wc output.txt")
				if output:
					output = "Leaks for command: [cyan]./pipex infile.txt cat wc output.txt[/cyan]\n" + output
			else:
				output1 = has_leaks("./pipex infile.txt cat cat ls cat wc output.txt")
				if output1:
					output = "Leaks for command: [cyan]./pipex infile.txt cat cat ls cat wc output.txt[/cyan]\n" + output1	
				output2 = has_leaks("./pipex here_doc EOF cat wc output.txt", input="line1\nline2\nEOF\n")
				if output2:
					output += "\nLeaks for command: [cyan]./pipex here_doc EOF cat wc output.txt[/cyan] with input: 'line1\\nline2\\nEOF\\n' \n" + output2	
			if output:
				console.print("Leaks: KO", style="red", end="")
				return [["leaks", output]]
			else:
				console.print("Leaks: OK", style="green", end="")
				return []
		except LeakException:
			return []

	def __test_sleep(self, test):
		_, pipex, _ = get_commands(test)
		start = time.time()
		try:
			run_bash(pipex, test, 5)
		except TimeoutExpired:
			pass
		elapsed = time.time() - start
		if elapsed < 2.8 or elapsed > 3.2:
			console.print(f"[red]{test.id}.KO ", end="")
			problems = [["time elapsed", "3s", f"{elapsed:.2f}s"]]
		else:
			console.print(f"[green]{test.id}.OK ", end="")
			problems = []
		return [test, problems]

	def execute_batch(self, is_bonus=False):
		tests = self.get_tests(is_bonus)
		shutil.copy(self.temp_dir / ".." / 'pipex', self.temp_dir)

		result = []
		for test in tests:
			res = self.execute_test(test)
			if res[1]:
				console.print(f"[red]{test.id}.KO ", end="")
			else:
				console.print(f"[green]{test.id}.OK ", end="")
			result.append(res)
		os.chdir(self.temp_dir)

		return result

	def show_error(self, result):
		if result[0] == "leaks":
			console.print(result[1])
			return
		_, pipex, path = get_commands(result[0])
		console.print(f"For: [cyan]{pipex}[/cyan]")
		if result[0].input:
			console.print("with input: " + escape_str(result[0].input))

		if (path != "default"):
			if path == None:
				console.print(f"with no PATH set")
			else:
				console.print(f"with PATH: \"{path}\"")

		console.print("[b red]Error[/b red]: " + result[0].description)

		table = Table(box=box.MINIMAL_HEAVY_HEAD, pad_edge=False, show_lines=True)

		table.add_column("", no_wrap=True)
		table.add_column("native")
		table.add_column("pipex")

		for error in result[1]:
			table.add_row(error[0], error[1], error[2])
		console.print(table)

		console.print()

	def show_test_results(self, results):
		with console.capture() as capture:
			errors = False
			for result in results:
				if result[1]:
					self.show_error(result)
					errors = True
		str_output = capture.get()
		if errors:
			show_errors_str(str_output, self.temp_dir, 20)
		return errors

	def execute_test(self, test):
		native, pipex, _ = get_commands(test)
		#execute native
		self.reset_test(test)
		native = run_bash(native, test, get_timeout())
		with open_ascii("outfile.txt") as r:
			native_outfile = r.read()

		#execute pipex
		self.reset_test(test)
		try:
			pipex = run_bash(pipex, test, get_timeout())
			with open_ascii("outfile.txt") as r:
				pipex_outfile = r.read()
		except TimeoutExpired:
			return [test, [["Timeout reached", "", "The command appears to be stuck"]]]

		return self.compare_output(test, native, native_outfile, pipex, pipex_outfile)

	def reset_test(self, test):
		os.chdir(self.temp_dir)
		dirpath = self.temp_dir / ".." / 'temp'
		if dirpath.exists() and dirpath.is_dir():
			shutil.rmtree(dirpath)
		shutil.copytree(".", '../temp')
		os.chdir('../temp')
		os.chmod("no_r_perm", 0o333)
		os.chmod("no_w_perm", 0o555)

	def compare_output(self, test, native: CompletedProcess, native_outfile, pipex, pipex_outfile):

		def diff_stderr(stderr, actual_stderr):
			errs = sorted(stderr.lower().splitlines())
			actual_errs = stderr.lower().splitlines()
			for line in errs:
				split = line.split(":")
				if len(split) < 3:
					continue
				cmd, msg = map(str.strip, split[1:])
				line = next(filter(lambda line: cmd in line, actual_errs), None)
				if line is None:
					return True
				if msg not in line:
					return True
			return False

		problems = []
		if diff_stderr(native.stderr, pipex.stderr):
			problems.append(
			    ["stderr\nNeeds to have the same message\nand command/filename", native.stderr, pipex.stderr])
		if native.returncode != pipex.returncode != 0:
			problems.append(["return code", str(native.returncode), str(pipex.returncode)])
		if native_outfile != pipex_outfile:
			problems.append(["outfile content", native_outfile, pipex_outfile])
		return [test, problems]

	def get_tests(self, exec_b):
		mandatory = [
		    TestCase(1, ['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             'Normal parameters, simple commands, everything should go ok'),
		    TestCase(2, ['infile.txt', 'cat', 'wc', 'inexistent.txt'], "Output file does not exist"),
		    TestCase(3, ['infile.txt', 'sed    "s/And/But/"', 'grep But', 'outfile.txt'],
		             'Normal parameters, commands with arguments, everything should go ok'),
		    TestCase(4, ['infile.txt', 'sed "s/And/But/"', "awk '{count++} END {print count}'", 'outfile.txt'],
		             'program that has spaces in the middle of string argument with single quotes (awk argument)'),
		    TestCase(5, ['infile.txt', 'sed "s/And/But/"', 'awk "{count++} END {print count}"', 'outfile.txt'],
		             'program that has spaces in the middle of string argument with double quotes (awk argument)'),
		    TestCase(
		        6, [
		            'infile.txt', 'sed "s/And/But/"', 'awk "{count++} END {printf \\"count: %i\\" , count}"',
		            'outfile.txt'
		        ],
		        'Argument with escaped double quotes and then a space [yellow](\\" ,)[/yellow], inside double quotes (awk argument)'
		    ),
		    TestCase(
		        7,
		        ['infile.txt', 'sed "s/And/But/"', "awk '{count++} END {printf \"count: %i\", count}'", 'outfile.txt'],
		        'program that has double quotes inside single quotes (awk argument)'),
		    TestCase(8, ['infile.txt', "./script.sh", 'wc', 'outfile.txt'], 'Command that is in the same folder'),
		    TestCase(9, ['infile.txt', './"script space.sh"', 'wc', 'outfile.txt'],
		             'The script is in the same folder, but has a name that contains a space with double quotes'),
		    TestCase(10, ['infile.txt', './"script\\"quote.sh"', 'wc', 'outfile.txt'],
		             'The script is in the same folder, but has a name that contains an escaped quote'),
		    TestCase(11, ['infile.txt', "./'script space.sh'", 'wc', 'outfile.txt'],
		             'The script is in the same folder, but has a name that contains a space with single quotes'),
		    TestCase(12,
		             ['infile.txt', str((self.tests_dir / "script.sh").resolve()), 'wc', 'outfile.txt'],
		             'Command that contains the complete path'),
		    TestCase(13, ['no_in', 'cat', 'wc', 'outfile.txt'], "Input files does not exist"),
		    TestCase(14, ['infile.txt', 'non_existent_comm', 'wc', 'outfile.txt'], "first command does not exist"),
		    TestCase(15, ['infile.txt', 'cat', 'non_existent_comm', 'outfile.txt'], "second command does not exist"),
		    TestCase(16, ['no_r_perm', 'cat', 'wc', 'outfile.txt'], "Input files does not have read permissions"),
		    TestCase(17, ['infile.txt', 'cat', 'wc', 'no_w_perm'], "Output files does not have write permissions"),
		    TestCase(18, ['infile.txt', './no_x_script.sh', 'wc', 'outfile.txt'],
		             "The first command does not have execution permission"),
		    TestCase(19, ['infile.txt', 'cat', './no_x_script.sh', 'outfile.txt'],
		             "The second command does not have execution permission"),
		    TestCase(20, ['infile.txt', './middle_fail.sh', 'wc', 'outfile.txt'],
		             "The first commands fails in the middle of executing, but produces some output"),
		    TestCase(21, ['infile.txt', 'cat', './middle_fail.sh', 'outfile.txt'],
		             "The second commands fails in the middle of executing, but produces some output"),
		    TestCase(22, ['infile.txt', './script.sh', './script.sh', 'outfile.txt'],
		             "The PATH variable is empty, but the scrips are local",
		             path=""),
		    TestCase(23, ['infile.txt', 'cat', 'wc', 'outfile.txt'], "The PATH variable is empty", path=""),
		    TestCase(24, ['infile.txt', './script.sh', './script.sh', 'outfile.txt'],
		             "The PATH variable does not exist with local scripts",
		             path=None),
		    TestCase(25, ['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             "The PATH variable does not exist with normal commands",
		             path=""),
		    TestCase(26, ['infile.txt', 'cat', 'script.sh', 'outfile.txt'],
		             "Should not match local script if it does not have a dot before the name"),
		    TestCase(27, ['infile.txt', 'cat', 'uname', 'outfile.txt'],
		             "Should search the command by the directory order in PATH",
		             path=f"{self.tests_dir}:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"),
		    TestCase(28, ['infile.txt', 'cat', 'uname', 'outfile.txt'],
		             "Should search the command by the directory order in PATH",
		             path=f"/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:{self.tests_dir}"),
		    TestCase(29, ['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             "The PATH is shorter and does not have /usr/bin/ (and thus wc) in it",
		             path=f"/bin"),
		    TestCase(30, ['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             "The PATH has '/' at the end of each entry",
		             path="/:".join("/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin".split(':'))),
		    TestCase(31, ['infile.txt', 'subdir/script.sh', 'wc', 'outfile.txt'],
		             "It should execute commands in the subdirectory")
		]

		bonus = [
		    TestCase(32, ['infile.txt', 'cat', 'grep And', "cat -e", 'wc', 'outfile.txt'], "Multiple commands"),
		    TestCase(33, ['infile.txt', 'cat', 'grep And', "cat -e", 'wc', 'no_file.txt'],
		             "output file does not exist"),
		    TestCase(34, ['infile.txt', 'catasdasd', 'asdasd', 'sdfsdf', 'fsdgss', 'outfile.txt'],
		             "Multiple wrong commands"),
		    TestCase(35, ['here_doc', '"EOF"', 'cat', 'cat -e', 'no_file.txt'],
		             "heredoc where output file does not exist",
		             input="teste\nsome_str\nEOF\n"),
		    TestCase(36, ['here_doc', '""', 'cat', 'cat -e', 'outfile.txt'],
		             "heredoc with empty string, but multiple lines",
		             input="teste\nsome_str\n\n"),
		    TestCase(37, ['here_doc', '""', 'cat', 'cat -e', 'outfile.txt'],
		             "heredoc with empty string, with only and enter",
		             input="\n"),
		    TestCase(38, ['here_doc', '"end of line"', 'cat', 'cat -e', 'outfile.txt'],
		             "heredoc with empty string, with only and enter",
		             input="bla\n\nEnd\nend of line\n"),
		    TestCase(39, ['here_doc', 'EOF', 'cat', 'cat -e', 'outfile.txt'],
		             "heredoc with EOF string, but with lines starting and ending in EOF",
		             input="Teste\nEOFx\nEOF some\nx EOF\nEOF\n"),
		]
		result = mandatory
		if exec_b:
			result += bonus
		return result
