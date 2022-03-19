from datetime import datetime, timedelta
from pathlib import Path
import ssl
import certifi
from urllib.request import urlopen
from git import Repo

import toml
from rich import print

from packaging import version as vs
from utils.Utils import REPO_URL
from version import version as current

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
toml_path = Path(__file__, "../update.toml").resolve()


def save_settings(settings):
	with open(toml_path, 'w') as f:
		toml.dump(settings, f)


def ignore_this_new_version(settings, new_version):
	settings['paco']['ignored'] = new_version
	save_settings(settings)


def do_not_update_ever(settings):
	settings['paco']['do_not_update'] = True
	save_settings(settings)


def get_settings():
	try:
		settings = toml.load(toml_path)
	except:
		settings = {'paco': {'last_run': None}}

def update_paco():
	settings = get_settings()
	if settings['paco'].get('do_not_update', False):
		return
	if settings['paco'].get('always', False):
		do_update()

	last_run = settings['paco']['last_run']
	# last_run and datetime.strptime(last_run, DATETIME_FORMAT) > datetime.now() - timedelta(hours=1):
	# 	return save_settings(settings)
	settings['paco']['last_run'] = datetime.strftime(datetime.now(), DATETIME_FORMAT)

	with urlopen(REPO_URL + "utils/version.py", context=ssl.create_default_context(cafile=certifi.where())) as data:
		new_version = data.read().decode("utf-8").split('"')[1]

	if (vs.parse(current) >= vs.parse(new_version) or
	    vs.parse(settings['paco'].get('ignored', '0.0.0')) >= vs.parse(new_version)):
		return save_settings(settings)

	print("There is a new version of francinette, do you wish to update?")
	while (True):
		choice = input("[Y]es / [N]o / [A]lways / [D]o not update ever: ").lower()
		if choice.startswith('y'):
			break
		if choice.startswith('n'):
			return ignore_this_new_version(settings, new_version)
		if choice.startswith('d'):
			return do_not_update_ever(settings)
		if choice.startswith('a'):
			settings['paco']['always'] = True
			break
		else:
			print("Please select one of the available options")
	save_settings(settings)
	do_update()

def do_update():
	repo = Repo(Path(__file__).parent.parent.resolve())
	origin = repo.remote()
	for fetch_info in origin.fetch(progress=)
	pass