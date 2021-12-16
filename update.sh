#!/bin/bash

cd $HOME

mkdir temp_____

# download zip
curl -L0 https://github.com/xicodomingues/francinette/archive/refs/heads/master.zip -o ~/temp_____/francinette.zip
cd temp_____

unzip -qq francinette.zip

mv francinette-master francinette
rm -rf francinette/c00
rm -rf francinette/files

cd $HOME/francinette

cd $HOME/temp_____
cp -r francinette ..

cd $HOME
rm -rf temp_____

echo "\033[1;37mFrancinette is updated. You can use it again!\033[0m"