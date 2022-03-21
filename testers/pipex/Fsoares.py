from dataclasses import dataclass
import logging
import os
from pathlib import Path
import shutil
from typing import List
from subprocess import CompletedProcess, run

from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import console
from utils.TraceToLine import open_ascii
from rich.table import Table
from rich import box
from halo import Halo

from utils.Utils import show_errors_file
from distutils.dir_util import copy_tree

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
	pipex = f'./pipex {infile} "{cmd1}" "{cmd2}" {outfile}'
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
		console.print("", style="default")
		os.chdir(self.temp_dir)

		has_errors = self.show_test_results(result)
		return [self.name] if has_errors else []

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
			with open('error_color.log', 'w', encoding='utf-8') as f:
				f.write(str_output)
			show_errors_file(self.temp_dir, "error_color.log", "errors.log", 20)
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
		problems = []
		if native.stdout != pipex.stdout:
			problems.append(["stdout", native.stdout, pipex.stdout])
		if len(native.stderr.splitlines()) != len(pipex.stderr.splitlines()):
			problems.append(["stderr", native.stderr, pipex.stderr])
		if (native.returncode == 0 and pipex.returncode != 0) or (native.returncode != 0 and pipex.returncode == 0):
			problems.append(["return code", str(native.returncode), str(pipex.returncode)])
		if native_outfile != pipex_outfile:
			problems.append(["outfile content", native_outfile, pipex_outfile])
		return [test, problems]

	def get_tests(self):
		return [
		    TestCase(['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             'Normal parameters, simple commands, everything should go ok'),
		    TestCase(['infile.txt', 'cat', 'wc', 'inexistent.txt'], "Output file does not exist"),
		    TestCase(['infile.txt', 'sed "s/And/But/"', 'grep But', 'outfile.txt'],
		             'Normal parameters, commands with arguments, everything should go ok'),
		    TestCase(['infile.txt', "./script.sh", 'wc', 'outfile.txt'], 'Command that is in the same folder'),
		    TestCase(['infile.txt', (self.tests_dir / "script.sh").resolve(), 'wc', 'outfile.txt'],
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
		             "The PATH is shorter and does not have /usr/bin/ (and this wc) in it",
		             path=f"/bin"),
		    TestCase(['infile.txt', 'cat', 'wc', 'outfile.txt'],
		             "The PATH has '/' at the end of each entry",
		             path="/:".join("/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin".split(':'))),
		    TestCase(['infile.txt', 'subdir/script.sh', 'wc', 'outfile.txt'],
		             "It should execute commands in the subdirectory")
		]
