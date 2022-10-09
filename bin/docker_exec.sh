#!/bin/bash
DIR="$( cd "/root/francinette" >/dev/null 2>&1 && pwd )"

current_dir=$PWD

cd "$current_dir" || exit

python3 "$DIR"/main.py "$@"
