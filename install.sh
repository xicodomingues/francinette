#!/bin/bash

cd "$HOME" || exit

mkdir temp_____

# download zip
curl -L0 https://github.com/xicodomingues/francinette/archive/refs/heads/master.zip -o ~/temp_____/francinette.zip
cd temp_____ || exit

unzip -qq francinette.zip

mv francinette-master francinette
cp -r francinette ..

cd "$HOME" || exit
rm -rf temp_____

cd "$HOME"/francinette || exit

# start a venv inside francinette
python3 -m venv venv

# activate venv
source venv/bin/activate

# install requirements
pip3 install -r requirements.txt

# set up the alias
if ! grep "francinette=" ~/.zshrc &> /dev/null; then
	echo "francinette alias not present"
	printf "\nalias francinette=~/francinette/tester.sh\n" >> ~/.zshrc
fi

if ! grep "paco=" ~/.zshrc &> /dev/null; then
	echo "Short alias not present. Adding it"
	printf "\nalias paco=%s/francinette/tester.sh\n" "$HOME" >> ~/.zshrc
fi

# print help
"$HOME"/francinette/tester.sh --help

echo -e "\033[1;37mPlease close this terminal window and open the terminal again for francinette to work\033[0m"