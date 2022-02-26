from email.mime import base
import logging
import random
import re
import string
from testers.BaseExecutor import BaseExecutor
from utils.TerminalColors import TC
from utils.Utils import show_errors_file
from halo import Halo

logger = logging.getLogger('pf-fsoares')


class Fsoares(BaseExecutor):

	name = "fsoares"
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)

	def execute(self):
		text = self.get_info_message("Preparing tests")
		with Halo(text=text) as spinner:
			self.gen_tests_mandatory()
			self.add_sanitizer_to_makefiles()
			self.call_make_command(f"build_m", self.exec_mandatory, silent=True, spinner=spinner)
			if spinner.enabled:
				spinner.succeed()
			else:
				raise Exception(f"{TC.RED}Problem compiling the tests{TC.NC}")

		errors = self.check_errors(self.run_tests("./printf.out"))
		logger.info(f"errors: {errors}")
		if errors:
			show_errors_file(self.temp_dir, "error_color.log", "errors.log")
		return errors

	def gen_tests_mandatory(self):

		def get_rand_str(n_min, n_max):
			return ''.join(random.choices(string.printable, k=random.randint(n_min, n_max))) \
					 .replace('\\', '\\\\') \
					 .replace('??', r'?\?') \
					 .replace('"', r'\"') \
					 .replace('\t', r'\t') \
					 .replace('\n', r'\n') \
					 .replace('\f', r'\f') \
					 .replace('\v', r'\v') \
					 .replace('\r', r'\r')

		def generate_random_formats():

			def random_int():
				return str(random.randint(-2**31, 2**31 - 1))

			def random_pointer():
				return "(void *)" + str(random.randint(-2**63, 2**63 - 1))

			def random_str():
				return '"' + get_rand_str(0, 1000) + '"'

			generators = {
			    'c': random_int,
			    's': random_str,
			    'p': random_pointer,
			    'd': random_int,
			    'i': random_int,
			    'u': random_int,
			    'x': random_int,
			    'X': random_int,
			    '%': lambda: '',
			}

			return random.choices(list(generators.items()), k=random.randint(2, 10))

		def get_format_str(args):

			def get_random_str():
				return get_rand_str(0, 10).replace('%', ' ')

			res = get_random_str()
			for arg in args:
				res += "%" + arg[0] + get_random_str()
			return res

		def get_arguments_str(args):
			return ", ".join([x for x in [arg[1]() for arg in args] if x != ''])

		def write_to_mandatory(lines):
			indicator = '//==%%^^&&++=='
			logger.info("reading mandatory")
			with open('mandatory.c') as m:
				content = m.read().replace(indicator, "\n\t\t".join(lines))
			logger.info(f'writing to mandatory')
			with open('mandatory.c', 'w') as m:
				m.write(content)

		base_template = 'test_printf_silent("##format", ##args);'

		lines = []
		for _ in range(1, 100):
			args = generate_random_formats()
			format_str = get_format_str(args)
			args_str = get_arguments_str(args)
			if args_str == '':
				continue
			lines.append(base_template.replace("##format", format_str).replace("##args", args_str))
		lines[-1] = lines[-1].replace("test_printf_silent", "test_printf")
		write_to_mandatory(lines)


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