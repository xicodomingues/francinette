#!/bin/bash

cd "$HOME" || exit

mkdir temp_____

if [ "$(uname)" != "Darwin" ]; then
	echo "Admin permissions need to install newer packages"
	sudo apt install libbsd-dev libncurses-dev
fi

cd temp_____ || exit
rm -rf francinette

# download github
echo "Downloading francinette repo..."
git clone --quiet --recursive https://github.com/xicodomingues/francinette.git 2> /dev/null

cp -r francinette .. 2> /dev/null

cd "$HOME" || exit
rm -rf temp_____

cd "$HOME"/francinette || exit

# activate venv
. venv/bin/activate

# install requirements
if ! pip3 install -r requirements.txt ; then
	echo "Problem launching the installer. Contact me (fsoares- on slack)"
	exit 1
fi

echo -e "\033[1;37mFrancinette is updated. You can use it again!\033[0m"
