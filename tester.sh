#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

current_dir=$PWD

# check for updates
version=68

cd "$current_dir" || exit
source "$DIR"/venv/bin/activate

python "$DIR"/main.py "$@"
