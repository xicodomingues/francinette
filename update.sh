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

cd "$HOME"/francinette || exit

cd "$HOME"/temp_____ || exit
cp -r francinette ..

cd "$HOME" || exit
rm -rf temp_____

if ! grep "paco=" ~/.zshrc &> /dev/null; then
	echo "Short alias 'paco' not present. Adding it"
	printf "\nalias paco=%s/francinette/tester.sh\n" "$HOME">> ~/.zshrc
fi

echo -e "\033[1;37mFrancinette is updated. You can use it again!\033[0m"