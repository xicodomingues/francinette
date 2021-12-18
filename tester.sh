#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

version=0

source $DIR/venv/bin/activate

MAIN_FILES_DIR=
PROJECTS_FILES_DIR=

python $DIR/main.py "$@"
