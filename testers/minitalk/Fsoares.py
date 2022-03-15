import logging
import re
import shutil
import subprocess
from signal import SIGINFO

import pexpect
from halo import Halo
from testers.BaseExecutor import BaseExecutor
from utils.TerminalColors import TC
from utils.Utils import open_ascii, show_errors_file

logger = logging.getLogger('mt-fsoares')


class Fsoares(BaseExecutor):

	name = "fsoares"
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		self.rewrite_mains()
		self.add_sanitizer_to_makefiles()
		# TODO: test mandatory
		# TODO: test bonus

		with Halo(self.get_info_message("Preparing tests")) as spinner:
			self.call_make_command('fclean all', self.exec_mandatory, silent=True, spinner=spinner)
		with Halo(self.get_info_message("Running tests")) as spinner:
			if self.test_leaks() != 0:
				spinner.fail()
				show_errors_file(self.temp_dir, "server.log", "errors.log", 20)
				return [self.name]

			spinner.succeed()
			print(f"{TC.GREEN}Tests OK!{TC.NC}")
			return []

	def test_leaks(self):
		server, server_pid = self.start_server()
		self.send_message(server_pid, "teste\n-----\n")
		server.expect("-----")
		self.send_signal(server_pid, "INFO")
		server.expect("reseted")
		self.send_message(server_pid, "A giant string that can be done as a teste to see if there is any memory leaks")
		self.send_message(server_pid,
		                  "v2 A giant string that can be done as a teste to see if there is any memory leaks")
		self.send_message(server_pid,
		                  "v4 A giant string that can be done as a teste to see if there is any memory leaks")
		self.send_message(server_pid, "\n=====\n")
		server.expect("=====")
		self.send_signal(server_pid, "INT")
		server.expect("==leaks==")
		result = server.wait()
		shutil.copy2(self.temp_dir / '../__my_srcs/server.log', self.temp_dir)
		shutil.copy2(self.temp_dir / '../__my_srcs/server', self.temp_dir)
		return result

	def start_server(self):

		def get_server_pid():
			with open_ascii("my_server.log", "r") as log:
				return log.readline().split(' ')[1].strip()

		child = pexpect.spawn(str((self.temp_dir / '..' / '__my_srcs' / 'server').resolve()))
		child.logfile = open("my_server.log", "wb")
		child.expect("__PID: .*\n")
		return child, get_server_pid()

	def send_message(self, server_pid, message):
		client_path = str((self.temp_dir / '..' / '__my_srcs' / 'client').resolve())
		client = subprocess.run([client_path, str(server_pid), message], capture_output=True, text=True)
		logger.info(client)

	def send_signal(self, pid, signal):
		res = subprocess.run(["kill", f"-{signal}", pid], capture_output=True)
		logger.info(res)

	def rewrite_mains(self):
		main_regex = re.compile(r"^(?:int|void)\s+main\(([^\)]+)\).*$")

		def rewrite_main(file):
			with open(file, 'r') as f:
				content = f.readlines()
			no_args = False
			for i, line in enumerate(content):
				match = main_regex.match(line)
				if match:
					args = match.group(1)
					if "void" in args:
						no_args = True
					content[i] = line.replace("main", "__main2")
			with open("wrapper_code.c") as wrap:
				to_add = wrap.readlines()
				for i, line in enumerate(to_add):
					if '//**main_here' in line:
						if no_args:
							to_add[i] = "\t__main2();\n"
						else:
							to_add[i] = "\t__main2(argn, args);\n"
			content += to_add
			with open(file, 'w') as f:
				f.writelines(content)

		p = subprocess.run('grep --include=\*.{c,h} -rnw ../__my_srcs -e "\\bmain\\b"',
		                   capture_output=True,
		                   shell=True,
		                   text=True)
		for file in [line.split(":")[0] for line in p.stdout.splitlines()]:
			rewrite_main(file)
