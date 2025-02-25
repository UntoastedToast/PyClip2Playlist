#!/bin/bash

echo "Building and publishing PyClip2Playlist to PyPI..."

echo -e "\nStep 1: Cleaning previous builds..."
cd ..
rm -rf dist/ build/ pyclip2playlist.egg-info/

echo -e "\nStep 2: Installing/Upgrading build tools..."
python -m pip install --upgrade pip
python -m pip install --upgrade build twine

echo -e "\nStep 3: Building package..."
python -m build

echo -e "\nStep 4: Checking distribution with twine..."
python -m twine check dist/*

echo -e "\nStep 5: Uploading to PyPI..."
echo "Note: You will need to enter your PyPI username and password"
python -m twine upload dist/*

echo -e "\nDone! If successful, the package can now be installed with:"
echo "pip install pyclip2playlist"
echo
read -p "Press Enter to exit..."
