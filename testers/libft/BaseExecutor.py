
import logging
import os
import re
import subprocess

from main import CT

logger = logging.getLogger()
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def remove_ansi_colors(text):
	return ansi_escape.sub('', text)



class BaseExecutor:
	def compile_with(self, command):
		if type(command) is str:
			command = command.split(" ")
		os.chdir(self.temp_dir)
		logger.info(f"On directory {os.getcwd()}")

		print(f"\n{CT.CYAN}Compiling tests from: {CT.WHITE}{self.folder}{CT.NC}", end="")
		if self.git_url:
			print(f" {self.git_url}):", end="")
		print()

		print(" ".join(command))
		p = subprocess.Popen(command)
		p.wait()
		return p