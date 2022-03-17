#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

current_dir=$PWD

# check for updates
version=67

cd "$HOME"/francinette || exit

git_url='https://raw.githubusercontent.com/xicodomingues/francinette/master'
curl -sS "$git_url/tester.sh" -o new_tester

new_version=$(grep -E '^version=\d+' new_tester)
rm new_tester

new_version="${new_version:8}"

launch_update()
{
	cd "$HOME" || exit
	curl "$git_url/utils/update.sh" -o new_francinette_update.sh
	bash new_francinette_update.sh
	rm -f new_francinette_update.sh
}

cd "$HOME"/francinette || exit
if [[ (! -e donotupdate) && ($new_version -gt $version) ]]; then
	if [[ -e alwaysupdate ]]; then
		launch_update
	else
		while true; do
			echo "There is a new version of francinette, do you wish to update?"
			read -r -p "[Y]es / [N]o / [A]lways / [D]o not update ever: " yn
			case $yn in
				[Yy]* ) launch_update; break ;;
				[Dd]* ) touch donotupdate; break ;;
				[Aa]* ) touch alwaysupdate; launch_update; break ;;
				[Nn]* ) break ;;
				* ) echo "Please answer yes, no, always, or don't ask again." ;;
			esac
		done
	fi
fi

cd "$current_dir" || exit
source "$DIR"/venv/bin/activate

python "$DIR"/main.py "$@"
