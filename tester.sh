#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

current_dir=$PWD

# check for updates
version=5

cd $HOME/francinette

curl -sS "https://raw.githubusercontent.com/xicodomingues/francinette/master/tester.sh" -o new_tester 2>&1 > /dev/null

new_version=$(grep -E '^version=\d+' new_tester)
rm new_tester

new_version="${new_version:8}"

cd $HOME/francinette
if [[ (! -e donotupdate) && ($new_version -gt $version) ]]; then
	while true; do
		read -p "There is a new version of francinette, do you wish to update? ([Y]es/[N]o/[D]on't ask again): " yn
		case $yn in
			[Yy]* ) source update.sh; break;;
			[Dd]* ) touch donotupdate; break;;
			[Nn]* ) break;;
			* ) echo "Please answer yes, no or don't ask again.";;
		esac
	done
fi

cd $current_dir
source $DIR/venv/bin/activate

python $DIR/main.py "$@"
