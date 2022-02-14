#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
base=$(dirname "$SCRIPT_DIR")

cd $base || exit

if [[ $1 == "-f" ]]; then
	force=1
fi

update_utils()
{
	DIR=$1
	changes=$(git diff --quiet $DIR/utils || printf "changed" )
	if [[ $changes == "changed" && $force -ne 1 ]]; then
		echo "$DIR has changes!"
	else
		cp -r "$base"/tests/utils $DIR
	fi
}

update_utils tests/libft/fsoares
update_utils tests/get_next_line/fsoares
update_utils tests/printf/fsoares
