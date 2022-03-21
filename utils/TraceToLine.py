import logging
import re
import subprocess

from halo import Halo

from utils.TerminalColors import TC

LLDB_TRACE_LIMIT = 50

trace_regex = re.compile(r"^\d+\s+([\w.?]+)\s+0x[\da-f]+ (\w+) \+ (\d+)")
lldb_out_regex = re.compile(r"\s+Summary: [\w.]+`(\w+) \+ (\d+) at (.*)$")
program_name_start = "##==##==##&&##==##==##"

logger = logging.getLogger('lldb')


def open_ascii(file, mode='r'):
	return open(file, mode, encoding='ascii', errors="backslashreplace")


def open_utf8(file, mode='r'):
	return open(file, mode, encoding='utf-8', errors="backslashreplace")


class TraceToLine:

	def __init__(self, temp_dir, error_file) -> None:
		self.remaining_lines = LLDB_TRACE_LIMIT
		self.temp_dir = temp_dir
		self.error_file = error_file

	def _write_to_error_file(self, lines, lines_map, traces):
		if len(lines_map) == 0:
			return lines
		for e_line, t_line_info in lines_map.items():
			t_prog, t_line = t_line_info
			if t_line == -1:
				lines[e_line] = ""
			if t_line != -1:
				lines[e_line] = traces[t_prog][t_line]

				self.remaining_lines -= 1
		return lines

	def _parse_lldb_out(self, lldb_out: str):
		def before_your_line(line):
			return (line.startswith("in malloc ")
					or line.startswith("in free ")
					or re.match("in (?:pf_)?sig(?:abort|segv|bus|alarm) (?:pf_)utils", line)
					or line.startswith("in _write "))
		def get_file_line(line):
			match = lldb_out_regex.match(line)
			if match:
				return "in " + match.group(1) + " " + match.group(3)

		stack_traces = []
		highlight_next = False
		for line in [get_file_line(line) for line in lldb_out.splitlines()]:
			if line:
				is_my_framework = before_your_line(line);
				if highlight_next and not is_my_framework:
					line = TC.YELLOW + "  -> " + line + TC.NC
					highlight_next = False
				else:
					line = "     " + line
				if is_my_framework:
					highlight_next = True
				stack_traces.append(line + '\n')
		return stack_traces

	def _get_traces(self, to_lldb):
		traces = dict()
		for program, lldb_lines in to_lldb.items():
			if len(lldb_lines) < 3:
				continue
			lldb_file_name = f"{program.replace('.', '_')}_lldb_commands"
			with open(self.temp_dir / lldb_file_name, 'w') as lldbf:
				lldbf.writelines(lldb_lines)
			p = subprocess.run(f"lldb {program} -s {lldb_file_name} --batch | tee {lldb_file_name}.out",
			                   shell=True,
			                   capture_output=True,
			                   text=True)
			logger.info(p)
			traces[program] = self._parse_lldb_out(p.stdout)
		return traces

	def _transform(self, line):

		def is_ignorable(match):
			return (match.group(1).endswith(".dylib") or match.group(2).startswith("show_signal_msg") or
			        match.group(2) == "0x0" or (match.group(2) == "start" and match.group(3) == "1"))

		match = trace_regex.match(line)
		if match:
			if is_ignorable(match):
				return ''
			return f"image lookup --address {match.group(2)}+{match.group(3)}\n"
		return line

	def _create_map(self, lines):
		map_lines = dict()  # contains a map of line to (prog, lldb_line)
		to_lldb = dict()  # contains a map of (prog, [lines])
		current_prog = None
		j = 0
		for i, line in enumerate(lines):
			if line.startswith(program_name_start):
				if current_prog != None:
					to_lldb[current_prog] = to_add
				current_prog = line.replace(program_name_start, "").split("/")[-1].strip()
				lines[i] = ""
				to_add = to_lldb.get(current_prog, [])
				to_lldb[current_prog] = to_add
				j = len(to_add) - to_add.count("")
				continue
			trans = self._transform(line)
			if line != trans:
				if trans != '':
					map_lines[i] = (current_prog, j)
					j += 1
				else:
					map_lines[i] = (current_prog, -1)
				to_add.append(trans)
			if j > self.remaining_lines and "main " in line:
				break

		return (map_lines, to_lldb)

	def parse_stack_traces(self):
		with open_utf8(self.error_file) as bf:
			lines = bf.readlines()
		if (self.remaining_lines <= 0):
			return lines
		try:
			with Halo(f"{TC.CYAN}Processing output{TC.NC}"):
				lines_map, to_lldb = self._create_map(lines)
				traces = self._get_traces(to_lldb)
				return self._write_to_error_file(lines, lines_map, traces)
		except Exception as ex:
			logger.exception(ex)
			return lines
