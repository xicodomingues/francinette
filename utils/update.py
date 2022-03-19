
from datetime import datetime, timedelta
from urllib.request import urlopen

import toml
from rich import print

from utils.Utils import REPO_URL

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

settings = toml.load("pyproject.toml")

last_run = settings['paco']['last_run']
if last_run and datetime.strptime(last_run, DATETIME_FORMAT) > datetime.now() - timedelta(hours=1):
	exit()

data = urlopen(REPO_URL + "utils/version.py")