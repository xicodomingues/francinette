

import random
import re
import string
from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_timeout, is_strict
from utils.Utils import show_errors_file


class Fsoares(BaseExecutor):

	name = "fsoares"
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)\.([^ ]+)")


	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		print('aa', self.generate_random_formats())
		self.add_sanitizer_to_makefiles()
		errors = self.execute_make_command(f"build", self.exec_mandatory)
		if errors:
			show_errors_file(self.temp_dir, "error_color.log", "errors.log")
		return []

	def generate_random_formats(self):
		def random_int():
			return random.randint(-2**31, 2**31 - 1)

		def random_long():
			return random.randint(-2**63, 2**63 - 1)

		def random_str():
			return ''.join(random.choices(string.printable, k=random.randint(1, 1643)))

		generators = {
			'c' : random_int,
			's' : random_str,
			'p' : random_long,
			'd' : random_int,
			'i' : random_int,
			'u' : random_int,
			'x' : random_int,
			'X' : random_int,
			'%' : lambda: '%',
		}

		return random.choices(list(generators.items()), k=random.randint(2, 10))

	def generate_random_mandatory(self):
		base = 	"\t\ttest_printf(##format, ##arguments);\n"


"""
Test ideas:
	- %%c %%%c %c%c %<valid_flag>c => width, -
	- width: 0, 1 - 10, 10000

	printf("%05d\n", -123);  // Outputs -0123 (pad to 5 characters)
	printf("%.5d\n", -123);  // Outputs -00123 (pad to 5 digits)

	printf("|%0d|%0d|\n", 0, 1);   // Outputs |0|1|
	printf("|%.0d|%.0d|\n", 0, 1); // Outputs ||1|

	https://github.com/alelievr/printf-unit-test/blob/master/inc/source-generator.h
"""