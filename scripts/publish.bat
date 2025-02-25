@echo off
echo Building and publishing PyClip2Playlist to PyPI...

echo.
echo Step 1: Cleaning previous builds...
cd ..
if exist "dist" rd /s /q "dist"
if exist "build" rd /s /q "build"
if exist "pyclip2playlist.egg-info" rd /s /q "pyclip2playlist.egg-info"

echo.
echo Step 2: Installing/Upgrading build tools...
python -m pip install --upgrade pip
python -m pip install --upgrade build twine

echo.
echo Step 3: Building package...
python -m build

echo.
echo Step 4: Checking distribution with twine...
python -m twine check dist/*

echo.
echo Step 5: Uploading to PyPI...
echo Note: You will need to enter your PyPI username and password
python -m twine upload dist/*

echo.
echo Done! If successful, the package can now be installed with:
echo pip install pyclip2playlist
echo.
pause
