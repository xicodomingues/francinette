#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
base=$(dirname "$SCRIPT_DIR")/tests

cp -r "$base"/utils "$base"/get_next_line/fsoares
cp -r "$base"/utils "$base"/printf/fsoares
cp -r "$base"/utils "$base"/libft/fsoares
