#!/bin/bash

if [ "$(uname)" != "Darwin" ]; then
	echo "Admin permissions need to install newer packages"
	sudo apt install libbsd-dev libncurses-dev
fi

cd "$HOME"/francinette || exit

git fetch origin
git reset --hard origin
git submodule update --init

# activate venv
. venv/bin/activate

echo "Updating python dependencies..."
# install requirements
if ! pip3 install --disable-pip-version-check -q -r requirements.txt ; then
	echo "Problem updating francinette. Contact me (fsoares- on slack)"
	exit 1
fi

echo -e "\033[1;37mFrancinette is updated. You can use it again!\033[0m"
