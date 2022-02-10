#!/bin/bash

cd "$HOME"/Library || exit

echo "Deleting \"$(pwd)/Caches/\""
rm -rf Caches

cd "$HOME/Library/Application Support/Slack/Service Worker" || exit

echo "Deleting \"$(pwd)/CacheStorage/\""
rm -rf CacheStorage

cd "$HOME/Library/Application Support/Code" || exit

echo "Deleting \"$(pwd)/Cache/\""
rm -rf "Cache"

echo "Deleting \"$(pwd)/CachedData/\""
rm -rf "CachedData"

echo "Deleting \"$(pwd)/CachedExtensionVSIXs/\""
rm -rf "CachedExtensionVSIXs"

echo "Deleting \"$(pwd)/Service Worker/CacheStorage/\""
rm -rf "Service Worker/CacheStorage"