#!/bin/bash

cd "$HOME" || exit

mkdir temp_____

# download zip
curl -L0 https://github.com/xicodomingues/francinette/archive/refs/heads/master.zip -o ~/temp_____/francinette.zip
cd temp_____ || exit

unzip -qq francinette.zip

mv francinette-master francinette
rm -rf francinette/c00
rm -rf francinette/files

cd "$HOME"/temp_____ || exit
cp -r francinette ..

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