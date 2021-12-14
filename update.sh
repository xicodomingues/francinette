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

find $HOME/francinette -name "C??_Tester.py" -print0 | while read -d $'\0' file
do
    name=$(basename "$file")
    echo "Backing up $name to $name.backup"
	mv "$file" "$name.backup"
done

cd $HOME/temp_____
cp -r francinette ..

cd $HOME
rm -rf temp_____

echo "Francinette is updated. You can use it again!"