import logging
import os
from pipes import quote
import shutil
from dataclasses import dataclass
from subprocess import CompletedProcess, run
from typing import List

from halo import Halo
from rich import box
from rich.table import Table
from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import console
from utils.TraceToLine import open_ascii
from utils.Utils import show_errors_str

logger = logging.getLogger("pipex-fso")


def run_bash(command, path):
	my_env = os.environ.copy()
	if path != None:
		my_env["PATH"] = path
	if path == None:
		my_env.pop("PATH")
	return run(command, capture_output=True, shell="True", encoding="ascii", errors="backslashreplace", env=my_env)


@dataclass
class TestCase:
	params: List[str]
	description: str
	path: str = os.environ['PATH']


def get_commands(test: TestCase):
	infile, cmd1, cmd2, outfile = test.params
	native = f"< {infile} {cmd1} | {cmd2} > {outfile}"
	pipex = f'./pipex {infile} {quote(cmd1)} {quote(cmd2)} {outfile}'
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

	def execute(self):
		Halo(self.get_info_message("Executing tests")).info()
		tests = self.get_tests()
		shutil.copy(self.temp_dir / ".." / 'pipex', self.temp_dir)

		result = []
		for i, test in enumerate(tests):
			res = self.execute_test(test)
			if res[1]:
				console.print(f"[red]{i + 1}.KO ", end="")
			else:
				console.print(f"[green]{i + 1}.OK ", end="")
			result.append(res)
		console.print("\n", style="default")
		os.chdir(self.temp_dir)

		has_errors = self.show_test_results(result)
		return self.result(has_errors)

	def show_error(self, result):
		_, pipex, path = get_commands(result[0])
		console.print(f"For: [cyan]{pipex}[/cyan]")
		console.print("[b red]Error[/b red]: " + result[0].description)

		table = Table(box=box.MINIMAL_HEAVY_HEAD, pad_edge=False, show_lines=True)

		table.add_column("", no_wrap=True)
		table.add_column("native")
		table.add_column("pipex")

		for error in result[1]:
			table.add_row(error[0], error[1], error[2])
		console.print(table)

		if (path != "default"):
			if path == None:
				console.print(f"with no PATH set")
			else:
				console.print(f"with PATH: \"{path}\"")

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
		native = run_bash(native, test.path)
		with open_ascii("outfile.txt") as r:
			native_outfile = r.read()

		#execute pipex
		self.reset_test(test)
		pipex = run_bash(pipex, test.path)
		with open_ascii("outfile.txt") as r:
			pipex_outfile = r.read()

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

		def adapt_stderr(stderr, actual_stderr):
			if "No such file or directory" in actual_stderr:
				return stderr.replace("/bin/sh", "pipex")
			else:
				return stderr.replace("/bin/sh", "pipex").replace("No such file or directory", "command not found")

		problems = []
		if native.stdout != pipex.stdout:
			problems.append(["stdout", native.stdout, pipex.stdout])
		native_stderr = adapt_stderr(native.stderr, pipex.stderr)
		if native_stderr != pipex.stderr:
			problems.append(["stderr", native_stderr, pipex.stderr])
		if native.returncode != pipex.returncode != 0:
			problems.append(["return code", str(native.returncode), str(pipex.returncode)])
		if native_outfile != pipex_outfile:
			problems.append(["outfile content", native_outfile, pipex_outfile])
		return [test, problems]

	def get_tests(self):
		return [
		    TestCase(['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             'Normal parameters, simple commands, everything should go ok'),
		    TestCase(['infile.txt', 'cat', 'wc', 'inexistent.txt'], "Output file does not exist"),
		    TestCase(['infile.txt', 'sed    "s/And/But/"', 'grep But', 'outfile.txt'],
		             'Normal parameters, commands with arguments, everything should go ok'),
		    TestCase(['infile.txt', 'sed "s/And/But/"', "awk '{count++} END {print count}'", 'outfile.txt'],
		             'program that has spaces in the middle of string argument with single quotes (awk argument)'),
		    TestCase(['infile.txt', 'sed "s/And/But/"', 'awk "{count++} END {print count}"', 'outfile.txt'],
		             'program that has spaces in the middle of string argument with double quotes (awk argument)'),
		    TestCase([
		        'infile.txt', 'sed "s/And/But/"', 'awk "{count++} END {printf \\"count: %i\\" , count}"', 'outfile.txt'
		    ], 'Argument with escaped double quotes and then a space [yellow](\\" ,)[\yellow], inside double quotes (awk argument)'),
		    TestCase(
		        ['infile.txt', 'sed "s/And/But/"', "awk '{count++} END {printf \"count: %i\", count}'", 'outfile.txt'],
		        'program that has double quotes inside single quotes (awk argument)'),
		    TestCase(['infile.txt', "./script.sh", 'wc', 'outfile.txt'], 'Command that is in the same folder'),
		    TestCase(['infile.txt', './"script space.sh"', 'wc', 'outfile.txt'],
		             'The script is in the same folder, but has a name that contains a space with double quotes'),
		    TestCase(['infile.txt', './"script\\"quote.sh"', 'wc', 'outfile.txt'],
		             'The script is in the same folder, but has a name that contains an escaped quote'),
		    TestCase(['infile.txt', "./'script space.sh'", 'wc', 'outfile.txt'],
		             'The script is in the same folder, but has a name that contains a space with single quotes'),
		    TestCase(['infile.txt', str((self.tests_dir / "script.sh").resolve()), 'wc', 'outfile.txt'],
		             'Command that contains the complete path'),
		    TestCase(['no_in', 'cat', 'wc', 'outfile.txt'], "Input files does not exist"),
		    TestCase(['infile.txt', 'non_existent_comm', 'wc', 'outfile.txt'], "first command does not exist"),
		    TestCase(['infile.txt', 'cat', 'non_existent_comm', 'outfile.txt'], "second command does not exist"),
		    TestCase(['no_r_perm', 'cat', 'wc', 'outfile.txt'], "Input files does not have read permissions"),
		    TestCase(['infile.txt', 'cat', 'wc', 'no_w_perm'], "Output files does not have write permissions"),
		    TestCase(['infile.txt', './no_x_script.sh', 'wc', 'outfile.txt'],
		             "The first command does not have execution permission"),
		    TestCase(['infile.txt', 'cat', './no_x_script.sh', 'outfile.txt'],
		             "The second command does not have execution permission"),
		    TestCase(['infile.txt', './middle_fail.sh', 'wc', 'outfile.txt'],
		             "The first commands fails in the middle of executing, but produces some output"),
		    TestCase(['infile.txt', 'cat', './middle_fail.sh', 'outfile.txt'],
		             "The second commands fails in the middle of executing, but produces some output"),
		    TestCase(['infile.txt', './script.sh', './script.sh', 'outfile.txt'],
		             "The PATH variable is empty, but the scrips are local",
		             path=""),
		    TestCase(['infile.txt', 'cat', 'wc', 'outfile.txt'], "The PATH variable is empty", path=""),
		    TestCase(['infile.txt', './script.sh', './script.sh', 'outfile.txt'],
		             "The PATH variable does not exist with local scripts",
		             path=None),
		    TestCase(['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             "The PATH variable does not exist with normal commands",
		             path=""),
		    TestCase(['infile.txt', 'cat', 'script.sh', 'outfile.txt'],
		             "Should not match local script if it does not have a dot before the name"),
		    TestCase(['infile.txt', 'cat', 'uname', 'outfile.txt'],
		             "Should search the command by the directory order in PATH",
		             path=f"{self.tests_dir}:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"),
		    TestCase(['infile.txt', 'cat', 'uname', 'outfile.txt'],
		             "Should search the command by the directory order in PATH",
		             path=f"/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:{self.tests_dir}"),
		    TestCase(['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             "The PATH is shorter and does not have /usr/bin/ (and thus wc) in it",
		             path=f"/bin"),
		    TestCase(['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             "The PATH has '/' at the end of each entry",
		             path="/:".join("/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin".split(':'))),
		    TestCase(['infile.txt', 'subdir/script.sh', 'wc', 'outfile.txt'],
		             "It should execute commands in the subdirectory")
		]
