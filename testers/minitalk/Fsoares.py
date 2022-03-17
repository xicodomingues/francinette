import logging
import re
import shutil
import subprocess
import threading
from itertools import takewhile
from pipes import quote
from time import sleep

import pexpect
from halo import Halo
from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_timeout, has_bonus
from utils.TerminalColors import TC
from utils.Utils import escape_str, open_ascii, show_errors_file

logger = logging.getLogger('mt-fsoares')
UNRELIABLE_MSG = ("\nThis Tester is not super reliable, so executing again can solve the problem. " +
                  "You can also try to increase the sleep time inside your minitalk app.")


def get_server_pid(logfile):
	with open_ascii(logfile, "r") as log:
		return log.readline().split(' ')[1].strip()


def start_process(command, logfile):
	child = pexpect.spawn(command,
	                      logfile=open(logfile, "w", encoding="utf-8"),
	                      encoding="utf-8",
	                      timeout=get_timeout())
	child.expect("__PID: .*\n")
	return child, get_server_pid(logfile)


def wait_for(process, string):
	if process.expect([string, pexpect.TIMEOUT], timeout=get_timeout()) == 1:
		raise Exception("Problem with the threads." + UNRELIABLE_MSG)


class BgThread(threading.Thread):

	def __init__(self, command):
		self.stdout = None
		self.stderr = None
		self.pid = None
		self.command = command
		threading.Thread.__init__(self)

	def run(self):
		p = subprocess.Popen(self.command.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.pid = p.pid
		self.stdout, self.stderr = p.communicate()


class Fsoares(BaseExecutor):

	name = "fsoares"
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		with Halo(self.get_info_message("Preparing tests")) as spinner:
			self.rewrite_mains()
			self.add_sanitizer_to_makefiles()
			command = 'fclean all'
			if has_bonus():
				command = 'fclean bonus'
			output = self.call_make_command(command, self.exec_mandatory, silent=True, spinner=spinner)
			if output:
				raise f'Problem preprating the testes, please contact me at {TC.CYAN}fsoares{TC.NC} in slack'

		Halo(self.get_info_message("Running tests")).info()
		result = self.test_communication()
		if self.test_leaks() != 0:
			show_errors_file(self.temp_dir, "server.log", "errors.log", 20)
			result = False
		if result:
			print(f"{TC.GREEN}Tests OK!{TC.NC}")
			return []
		else:
			print(f"{TC.GREEN}Tests KO!{TC.NC}")
			return [self.name]

	def test_communication(self):
		server_thread = BgThread(str((self.temp_dir / '../__my_srcs/server')))
		server_thread.start()
		sleep(0.1)
		server_pid = str(server_thread.pid)
		middle, middle_pid = start_process(f"./middleman.out {server_thread.pid}", "middleman.log")

		message = "Test rand stuff ~(*123!@#$%^&*(_+-=][}{';:.></|?)"
		if has_bonus():
			message += " Ž (╯°□°)╯︵ ┻━┻"
		print(f'{TC.BLUE}Test string{TC.NC}: "{escape_str(message)}"')

		client_pid = self.send_message(middle_pid, '=====' + message + '=====\n')
		logger.info(f"client_pid: {client_pid}, server_pid: {server_pid}, middle_pid: {middle_pid}")
		self.send_signal(middle_pid, "INT")
		wait_for(middle, "=====")
		self.send_signal(middle_pid, "INT")
		self.send_signal(server_pid, "INT")
		server_thread.join(get_timeout())
		output = escape_str(server_thread.stdout.decode('utf-8', errors="backslashreplace").split("=====")[1])
		color = TC.GREEN
		if message not in output:
			color = TC.RED
		print(f'{color}Received   {TC.NC}: "{escape_str(output)}"')
		correct_signals = self.check_only_used_usr_signals(server_pid, client_pid)
		return color is not TC.RED and correct_signals

	def check_only_used_usr_signals(self, server_id, client_id):

		def check_process_signals(lines, proc_id):
			for line in lines:
				sig, pid = line.group(1), line.group(2)
				if pid == proc_id and sig != "30" and sig != "31":
					return False
			return True

		line_regex = re.compile(r"(\d+) from (\d+)")
		with open_ascii("middleman.log") as log:
			entries = [line_regex.match(line) for line in log.readlines() if line_regex.match(line)]
		logger.info(entries)
		only_usr = check_process_signals(entries, client_id)
		spinner = Halo("Client only uses SIGUSR1 and SIGUSR2: ", placement="right")
		spinner.succeed() if only_usr else spinner.fail()
		has_server_sigs = [entry for entry in entries if entry.group(2) == server_id]
		server_only_usr = True
		if has_server_sigs:
			server_only_usr = check_process_signals(entries, server_id)
			spinner = Halo("Server only uses SIGUSR1 and SIGUSR2: ", placement="right")
			spinner.succeed() if server_only_usr else spinner.fail()

		if has_bonus():
			spinner = Halo("Server sends client acknowledgements (bonus): ", placement="right")
			spinner.succeed() if has_server_sigs else spinner.fail()
		return only_usr and server_only_usr and (has_server_sigs if has_bonus() else True)

	def test_leaks(self):
		server, server_pid = start_process(str((self.temp_dir / '../__my_srcs/server').resolve()), 'my_server.log')
		self.send_message(server_pid, "teste\n-----\n")
		wait_for(server, "-----")
		self.send_signal(server_pid, "INFO")
		wait_for(server, "reseted")
		self.send_message(server_pid, "A giant string that can be done as a teste to see if there is any memory leaks")
		self.send_message(server_pid, "v2 A giant string that can be done as a teste to see if")
		self.send_message(server_pid, "v4 A giant string that can be done as a teste to see if")
		self.send_message(server_pid, "\n=====\n")
		wait_for(server, "=====")
		self.send_signal(server_pid, "INT")
		wait_for(server, "==leaks==")
		result = server.wait()
		shutil.copy2(self.temp_dir / '../__my_srcs/server.log', self.temp_dir)
		shutil.copy2(self.temp_dir / '../__my_srcs/server', self.temp_dir)
		return result

	def send_message(self, server_pid, message):
		client_path = str((self.temp_dir / '../__my_srcs/client').resolve())
		client = None
		try:
			client = subprocess.run(f'{client_path} {server_pid} {quote(message)}',
			                        capture_output=True,
			                        timeout=get_timeout(),
			                        shell=True)
			logger.info(client)
		except Exception as ex:
			raise Exception("Timeout when sending message to the server." + UNRELIABLE_MSG) from ex
		if client.stderr:
			error = client.stderr.decode('utf-8', errors="backslashreplace")
			error = takewhile(lambda line: "Shadow bytes around" not in line, error.splitlines())
			print("\n".join(error))
			raise Exception("Memory problems")
		return re.match(r"__PID: (\d+)", client.stdout.decode('utf-8', errors="backslashreplace")).group(1)

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
