

import re
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
		self.add_sanitizer_to_makefiles()
		errors = self.execute_make_command(f"build", self.exec_mandatory)
		if errors:
			show_errors_file(self.temp_dir, "error_color.log", "errors.log")
		return []

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