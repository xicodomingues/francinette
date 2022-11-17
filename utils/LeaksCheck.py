import logging
import re
import subprocess
import threading
from time import sleep
from utils.ExecutionContext import console

logger = logging.getLogger("leak-check")

leaks_regex = re.compile(".* (\d+) leak(?:s)? for (\d+) total.*")


class LeakException(Exception):
	pass


class LeakChecker(threading.Thread):

	def __init__(self, command, timeout=1, input=None):
		self.stdout = None
		self.stderr = None
		self.pid = None
		self.command = command
		self.return_code = None
		self.input = input
		self.timeout = timeout
		threading.Thread.__init__(self)

	def run(self):
		proc = subprocess.Popen(("leaks -q -atExit -- " + self.command).split(),
							errors="backslashreplace",
							stdout=subprocess.PIPE,
							stdin=subprocess.PIPE,
							stderr=subprocess.STDOUT)
		self.pid = str(proc.pid)
		self.stdout = ""
		if self.input:
			lines = self.input.splitlines(True)
			for line in lines:
				proc.stdin.write(line)
		proc.stdin.close()
		while True:
			line = proc.stdout.readline()
			self.stdout += line


def has_leaks(command, timeout=1.5, input=None):
	checker = LeakChecker(command, timeout, input=input)
	checker.daemon = True
	checker.start()
	sleep(1)
	if not checker.stdout:
		console.print("\nLeak check was not executed, do it manually\n", style="b yellow")
		raise LeakException()
	leaks = next(line for line in checker.stdout.splitlines() if leaks_regex.match(line))
	match = leaks_regex.match(leaks)
	if match.group(1) != "0":
		return checker.stdout
	return False
	