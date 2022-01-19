import logging
import re

from utils.TerminalColors import CT

logger = logging.getLogger()
ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def remove_ansi_colors(text):
	return ansi_escape.sub('', text)
