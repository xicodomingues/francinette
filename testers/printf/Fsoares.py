import itertools
import logging
import random
import os
import re
import string

from halo import Halo
from testers.BaseExecutor import BaseExecutor
from utils.ExecutionContext import get_context, is_strict
from utils.TerminalColors import TC
from utils.Utils import show_errors_file

logger = logging.getLogger('pf-fsoares')


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


def random_int():
	return str(random.randint(-2**31, 2**31 - 1))


def random_pointer():
	return "(void *)" + str(random.randint(-2**63, 2**63 - 1))


def random_str():
	return '"' + get_rand_str(0, 100) + '"'


def write_to(lines, file):
	indicator = '//==%%^^&&++=='
	logger.info(f"reading {file}")
	with open(file) as m:
		content = m.read().replace(indicator, "\n".join(lines))
	logger.info(f'writing to {file}')
	with open(file, 'w') as m:
		m.write(content)


class Fsoares(BaseExecutor):

	name = "fsoares"
	folder = 'fsoares'
	git_url = 'my own tests'
	line_regex = re.compile(r"^([^:]+):(.+)$")
	test_regex = re.compile(r"(\d+)(?:[^ ]+)?\.([^ ]+)")

	def __init__(self, tests_dir, temp_dir, to_execute, missing) -> None:
		super().__init__(tests_dir, temp_dir, to_execute, missing)
		if is_strict():
			get_context().args.timeout = str(int(get_context().args.timeout) * 10);
		# macOS: suppress inconsequential but intrusive
		# debug messages printed by Apple's libmalloc
		os.environ['MallocNanoZone'] = '0'

	def execute(self):
		text = self.get_info_message("Compiling tests")
		with Halo(text=text) as spinner:
			self.gen_tests_mandatory()
			if self.exec_bonus:
				self.generate_bonus()
			self.add_sanitizer_to_makefiles()
			self.call_make_command(f"build_m", self.exec_mandatory, silent=True, spinner=spinner)
			self.call_make_command(f"build_b", self.exec_bonus, silent=True, spinner=spinner)
			if not spinner.enabled:
				raise Exception(f"{TC.RED}Problem compiling the tests{TC.NC}")

		errors = self.check_errors(self.run_tests("./printf.out"))
		if self.exec_bonus:
			errors = set(errors).union(self.check_errors(self.run_tests("./printf_b.out", show_message=False)))
		logger.info(f"errors: {errors}")
		if errors:
			show_errors_file(self.temp_dir, "error_color.log", "errors.log", 20)
		else:
			if not is_strict():
				print(f"Want some more thorough tests? run '{TC.B_WHITE}francinette --strict{TC.NC}'.")
		return self.result(errors)

	def gen_tests_mandatory(self):

		def generate_random_formats():

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

		base_template = '\t\t/* ##i */ test_printf_silent("##format", ##args);'

		lines = []
		i = 0
		while i < 100:
			args = generate_random_formats()
			format_str = get_format_str(args)
			args_str = get_arguments_str(args)
			if args_str == '':
				continue
			i += 1
			lines.append(
			    base_template.replace("##format", format_str).replace("##args", args_str).replace("##i", str(i + 1)))
		lines[-1] = lines[-1].replace("test_printf_silent", "test_printf")
		write_to(lines, 'mandatory.c')

	def generate_bonus(self):
		base_template = '\t\t/* ##i */ test_printf_silent("##format", ##args);'

		formats = {
		    'c': ('-', ["'5'", "'x'", r"'\n'"]),
		    's': ('-.', ['(char *)NULL', '""', '"test"', r'"joihwhhgsdkhksdgsdg\t\v\n\r\f\a25252\b6"']),
		    'p': ('-', [
		        '(void *)0', '(void *)0xABCDE', '(void *)ULONG_MAX', '(void *)LONG_MIN', '(void *)-1', '(void *)-2352'
		    ]),
		    'd': ('-. 0+', [0, 5, -1, -10, 100, -1862, 'INT_MIN', 'INT_MAX']),
		    'i': ('-. 0+', [0, 5, -1, -10, 100, -1862, 'INT_MIN', 'INT_MAX']),
		    'u': ('-.0', [0, 5, -1, -10, 100, -1862, '0xABCDE', 'INT_MIN', 'INT_MAX', 'UINT_MAX']),
		    'x': ('-.0#', [0, 5, -1, -10, '0x1234', -1862, '0xABCDE', 'INT_MIN', 'INT_MAX', 'UINT_MAX']),
		    'X': ('-.0#', [0, 5, -1, -10, '0x1234', -1862, '0xABCDE', 'INT_MIN', 'INT_MAX', 'UINT_MAX']),
		    '%': ('', ['']),
		}

		entry_str = "%{minus}{zero}{space}{sharp}{plus}{width}{dot}{precision}{format}"
		i = 1
		lines = ["void test_c() {", f"\tTEST(\"c format\", {'{'}"]
		last_fmt = 'c'
		for fmt, minus, zero, space, sharp, plus, dot, width, precision in itertools.product(
		    'cspdiuxX%', ['', '-'], ['', '0'], ['', ' '], ['', '#'], ['', '+'], ['', '.'], ['', 1, 5, 10, 100],
		    ['', 0, 1, 5, 10, 100]):
			if minus and '-' not in formats[fmt][0]:
				continue
			if zero and '0' not in formats[fmt][0]:
				continue
			if sharp and '#' not in formats[fmt][0]:
				continue
			if space and ' ' not in formats[fmt][0]:
				continue
			if plus and '+' not in formats[fmt][0]:
				continue
			if plus and space:
				continue
			if zero and minus:
				continue
			if dot and '.' not in formats[fmt][0]:
				continue
			if dot != '.' and precision != '':
				continue
			if fmt == '%' and width:
				continue
			entry_fmt = entry_str.format(minus=minus,
			                             zero=zero,
			                             space=space,
			                             sharp=sharp,
			                             plus=plus,
			                             width=width,
			                             dot=dot,
			                             precision=precision,
			                             format=fmt)
			format_str = [entry_fmt for _ in formats[fmt][1]]
			arguments = [str(test) for test in formats[fmt][1]]
			if fmt == '%':
				arguments = ''
			if last_fmt != fmt:
				i = 1
				last_fmt = fmt
				lines[-1] = lines[-1].replace("test_printf_silent", "test_printf")
				lines.append("\t});")
				lines.append("}\n")
				lines.append(f"void test_{fmt if fmt != '%' else 'percent'}() {'{'}")
				lines.append(f"\tTEST(\"{fmt} format\", {'{'}")

			to_add = (base_template.replace("##format", ', '.join(format_str)).replace("##args",
			                                                                           ', '.join(arguments)).replace(
			                                                                               "##i", str(i)))
			if (i % 50 == 0):
				to_add = to_add.replace("test_printf_silent", "test_printf")
			if fmt == '%':
				to_add = to_add.replace(", );", ");").replace("test_printf_silent", "test_printf_silent_noarg")
			lines.append(to_add)
			i += 1
		lines[-1] = lines[-1].replace("test_printf_silent", "test_printf")
		lines.append("\t});")
		lines.append("}\n")
		write_to(lines, 'bonus.c')
