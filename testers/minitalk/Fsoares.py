import logging
import random
import re
import shutil
import string
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
from utils.Utils import decode_ascii, escape_str, open_ascii, show_errors_file

logger = logging.getLogger('mt-fsoares')
UNRELIABLE_MSG = ("\nThis Tester is not super reliable, so executing again can solve the problem. " +
                  "You can also try to increase the sleep time inside your minitalk app.")
MSG_DELIM = '====='

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
		self.return_code = None
		threading.Thread.__init__(self)

	def run(self):
		p = subprocess.Popen(self.command.split(), shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		self.pid = str(p.pid)
		self.stdout, self.stderr = p.communicate()
		self.return_code = p.returncode


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
			self.compile('fclean all', spinner)

		Halo(self.get_info_message("Running tests")).info()
		result = self.test_client_server()
		if has_bonus():
			print(f"{TC.PURPLE}\n[Bonus]{TC.NC}")
			self.compile('fclean bonus', None)
			result = self.test_client_server(bonus=True) and result
		return self.result(not result)

	def compile(self, command, spinner):
		output = self.call_make_command(command, self.exec_mandatory, silent=True, spinner=spinner)
		if output:
			raise f'Problem preprating the testes, please contact me at {TC.CYAN}fsoares{TC.NC} in slack'

	def test_client_server(self, bonus=False):
		no_leaks = self.test_leaks()
		res = no_leaks and self.test_messages(bonus)
		res = self.test_communication(bonus) and res
		if not no_leaks:
			show_errors_file(self.temp_dir, "leaks.log", "errors.log", 20)
		return res

	def start_bg_process(self, command):
		server_thread = BgThread(command)
		server_thread.start()
		sleep(0.1)
		return server_thread

	def start_server(self):
		return self.start_bg_process(str((self.temp_dir / '../__my_srcs/server')))

	def test_messages(self, bonus=False):
		message = "Test `~(*123!@#$%^&*(_+-=][}{';:.></|\\?)"
		if bonus:
			message += " Ž (╯°□°)╯︵ ┻━┻"
		return self.send_message_wrapper(message) and self.send_giant_message() and self.send_multiple_messages()

	def send_message_wrapper(self, message):
		server = self.start_server()
		try:
			print(f'{TC.BLUE}Test string{TC.NC}: "{message}"')
			self.send_message(server,MSG_DELIM + message + MSG_DELIM)
		finally:
			self.send_signal(server.pid, "INT")
			server.join(0.2)
		actual = server.stdout.decode("utf-8", errors="replace").split(MSG_DELIM)[1]
		color = TC.GREEN
		if (actual != message):
			color = TC.RED
		print(f'{color}Received   {TC.NC}: "{actual[:len(message)]}"')
		return actual == message

	def send_giant_message(self):

		def correctly_received(output, expected, spinner):

			def show_error(string, start, i, end):
				middle = string[i]
				after = string[i + 1:end]
				if middle == '\\' and string[i + 1] == 'x':
					middle = string[i:i + 3]
					after = string[i + 4:end]
				return (escape_str(string[start:i]) + TC.RED + escape_str(middle) + TC.NC + escape_str(after))

			actual = output.split(MSG_DELIM)[1]
			if actual != expected:
				for i, c in enumerate(actual):
					if c != expected[i]:
						if i < 10:
							part_ex = escape_str(expected[:i + 10]) + "..."
							part_ac = show_error(actual, 0, i, i + 10) + "..."
						elif i > len(actual) - 10:
							part_ex = "..." + escape_str(expected[i - 10:])
							part_ac = "..." + show_error(actual, i - 10, i, len(expected))
						else:
							part_ex = "..." + escape_str(expected[i - 10:i + 10]) + "..."
							part_ac = "..." + show_error(actual, i - 10, i, i + 10) + "..."
						spinner.fail()
						spinner.enabled = False
						print(f"At position {i}:\n{TC.BLUE}Expected{TC.NC}: \"{part_ex}\"\n" +
						      f"{TC.RED}Actual  {TC.NC}: \"{part_ac}\"")
						return False
			return True

		server = self.start_server()
		try:
			message = ''.join(random.choices(string.printable, k=5000))
			spinner = Halo("Sending 5000 characters: ", placement="right").start()
			self.send_message(server, MSG_DELIM + message + MSG_DELIM)
		finally:
			self.send_signal(server.pid, "INT")
			server.join(0.2)
		result = correctly_received(decode_ascii(server.stdout), message, spinner)
		if spinner.enabled:
			spinner.succeed() if result else spinner.fail()
		return result and server.return_code == 0

	def send_multiple_messages(self):
		with Halo("Multiple messages: ", placement="right") as spinner:
			server = self.start_server()
			messages = ["Hola", "Tudo bien?", "E como vai o tempo?", "vai andando"];
			try:
				for message in messages:
					self.send_message(server, MSG_DELIM + message + MSG_DELIM)
			finally:
				self.send_signal(server.pid, "INT")
				server.join(0.2)
			output = decode_ascii(server.stdout)
			for message in messages:
				if message not in output:
					spinner.fail()
					return False
			spinner.succeed()
			return True


	def test_communication(self, bonus=False):
		server = self.start_server()
		try:
			middle = self.start_bg_process(f"./middleman.out {server.pid}")
			client_pid = self.send_message(middle, "teste")
			logger.info(f"client_pid: {client_pid}, server_pid: {server.pid}, middle_pid: {middle.pid}")
		finally:
			sleep(0.2)
			self.send_signal(middle.pid, "INT")
			self.send_signal(server.pid, "INT")
			server.join(0.2)
			middle.join(1)
		return self.check_only_used_usr_signals(server.pid, client_pid, bonus, decode_ascii(middle.stdout))

	def check_only_used_usr_signals(self, server_id, client_id, bonus, output):

		def check_process_signals(lines, proc_id):
			for line in lines:
				sig, pid = line.group(1), line.group(2)
				if pid == proc_id and sig != "30" and sig != "31":
					return False
			return True

		line_regex = re.compile(r"(\d+) from (\d+)")
		entries = [line_regex.match(line) for line in output.splitlines() if line_regex.match(line)]
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

		if bonus:
			spinner = Halo("Server sends client acknowledgements: ", placement="right")
			spinner.succeed() if has_server_sigs else spinner.fail()
		return only_usr and server_only_usr and (bool(has_server_sigs) if bonus else True)

	def test_leaks(self):
		server = self.start_server()
		spinner = Halo("Leaks: ", placement="right").start()
		try:
			self.send_message(server, "teste\n-----\n")
			self.send_signal(server.pid, "INFO")
			self.send_message(server, "Hello!!")
			self.send_message(server, "Hello!!")
			self.send_message(server, "Hello!!")
		finally:
			self.send_signal(server.pid, "INT")
			server.join(0.2)

		shutil.copy2(self.temp_dir / '../__my_srcs/server', self.temp_dir)
		shutil.copy2(self.temp_dir / '../__my_srcs/server.log', self.temp_dir / 'leaks.log')
		spinner.succeed() if server.return_code == 0 else spinner.fail()
		return server.return_code == 0

	def send_message(self, server, message):

		def terminate_server():
			self.send_signal(server.pid, "INT")
			try:
				server.join(0.2)
			except:
				pass

		client_path = str((self.temp_dir / '../__my_srcs/client').resolve())
		client = None
		try:
			client = subprocess.run(f'{client_path} {server.pid} {quote(message)}',
			                        capture_output=True,
			                        timeout=get_timeout() * 2,
			                        shell=True)
			logger.info(client)
		except Exception as ex:
			terminate_server()
			raise Exception(
			    "Timeout when sending message to the server, please increase it with the --timeout option.") from ex
		if client.stderr:
			error = client.stderr.decode('utf-8', errors="backslashreplace")
			error = takewhile(lambda line: "Shadow bytes around" not in line, error.splitlines())
			print("\n".join(error))
			terminate_server()
			raise Exception("Memory problems")
		return re.match(r"__PID: (\d+)", client.stdout.decode('utf-8', errors="backslashreplace")).group(1)

	def send_signal(self, pid, signal):
		res = subprocess.run(["kill", f"-{signal}", pid], capture_output=True)
		logger.info(res)

	def rewrite_mains(self):
		main_regex = re.compile(r"^(?:int|void)\s+main\s*\(([^\)]+)\).*$")
		main_const_regex = re.compile(r"^(?:int|void)\s+main\s*\((.*,.*\bconst\b.*)\).*$")

		def rewrite_main(file):
			with open(file, 'r') as f:
				content = f.readlines()
			no_args = False
			const_main = False
			for i, line in enumerate(content):
				match = main_regex.match(line)
				if match:
					args = match.group(1)
					if "void" in args:
						no_args = True
					content[i] = line.replace("main", "__main2")
				if main_const_regex.match(line):
					const_main = True
			with open("wrapper_code.c") as wrap:
				to_add = wrap.readlines()
				for i, line in enumerate(to_add):
					if "int main(" in line and const_main:
						to_add[i] = "int main(int argn, char const *args[])"
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
