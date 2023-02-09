import logging
import signal
import subprocess
import sys
from pexpect import fdpexpect
import os
import io
from rich import status


logger = logging.getLogger("base")

def timeout_handler():
	raise BaseException("timeout")

def run(command: str, timeout: int):
	print("to print:", command, file=sys.stderr)
	p = subprocess.Popen(
		command,
		stdout=subprocess.PIPE,
		stdin=subprocess.PIPE,
		stderr=subprocess.PIPE,
		shell=True,
		executable="/bin/bash",
	)
	output = ""
	try:
		old_handler = signal.signal(signal.SIGALRM, timeout_handler)
		signal.alarm(timeout)
		reader = io.TextIOWrapper(p.stdout, encoding='utf8', errors="backslashreplace")
		while True:
			char = reader.read(1)
			output += char
			print(char, end="", flush=True)
			if p.poll() is not None:
				break;
		print("Done executing!!")
	except BaseException:
		print("timed out")
	finally:
		signal.signal(signal.SIGALRM, old_handler)
		signal.alarm(0)
	print(output)
		
#run_command('/Users/fsoares-/test/a.out', 3)