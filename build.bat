@echo off
echo Cleaning up previous build...
rmdir /s /q build dist
echo.

echo Installing requirements...
pip install -r requirements.txt
pip install pyinstaller
echo.

echo Building executable...
pyinstaller PyClip2Playlist.spec
echo.

if exist "dist\PyClip2Playlist.exe" (
    echo Build successful! The executable is in the dist folder.
    echo You can now run dist\PyClip2Playlist.exe
) else (
    echo Build failed! Check the error messages above.
)

pause
