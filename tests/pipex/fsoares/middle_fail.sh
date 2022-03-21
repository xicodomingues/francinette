#!/bin/bash

#read from stdin
while read line
do
  echo "$line"
done

echo "some other stuff"
echo "show some dummy error message" 1>&2

exit 13