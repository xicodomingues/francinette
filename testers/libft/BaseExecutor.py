
import logging
import os
import subprocess

from main import CT

logger = logging.getLogger()

class BaseExecutor:
	def compile_with(self, command):
		if type(command) is str:
			command = command.split(" ")
		os.chdir(os.path.join(self.temp_dir, self.folder))
		logger.info(f"On directory {os.getcwd()}")

		print(f"\n{CT.CYAN}Compiling tests from: {CT.WHITE}{self.folder}{CT.NC}", end="")
		if self.git_url:
			print(f" {self.git_url}):", end="")
		print()

		print(" ".join(command))
		p = subprocess.Popen(command)
		p.wait()
		return p