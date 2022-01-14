#!/bin/bash

cd "$HOME" || exit

mkdir temp_____

# download zip
curl -L0 https://github.com/xicodomingues/francinette/archive/refs/heads/master.zip -o ~/temp_____/francinette.zip
cd temp_____ || exit

if ! unzip -qq francinette.zip ; then
	echo "Please install unzip in your system"
	exit 1
fi

mv francinette-master francinette
cp -r francinette ..

cd "$HOME" || exit
rm -rf temp_____

cd "$HOME"/francinette || exit

# start a venv inside francinette
python3 -m venv venv

# activate venv
. venv/bin/activate

# install requirements
if ! pip3 install -r requirements.txt ; then
	echo "Problem launching the installer. Contact me (fsoares- on slack)"
	exit 1
fi

RC_FILE="$HOME/.bashrc"
if [[ -f "$HOME/.zshrc" ]]; then
	RC_FILE="$HOME/.zshrc"
fi

echo "try to add alias in file: $RC_FILE"

# set up the alias
if ! grep "francinette=" "$RC_FILE" &> /dev/null; then
	echo "francinette alias not present"
	printf "\nalias francinette=%s/francinette/tester.sh\n" "$HOME" >> "$RC_FILE"
fi

if ! grep "paco=" "$RC_FILE" &> /dev/null; then
	echo "Short alias not present. Adding it"
	printf "\nalias paco=%s/francinette/tester.sh\n" "$HOME" >> "$RC_FILE"
fi

# print help
"$HOME"/francinette/tester.sh --help

echo "Please close this terminal window and open the terminal again for francinette to work"