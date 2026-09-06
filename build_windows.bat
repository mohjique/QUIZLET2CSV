@echo off
REM Builds Quizlet2CSV.exe from source. Double-click this file to run it
REM after downloading/unzipping the project, and again any time you edit
REM the .py source or swap the icon.
setlocal

cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on PATH. Install it from https://python.org
    echo ^(check "Add python.exe to PATH" during setup^) and re-run this script.
    pause
    exit /b 1
)

python -m pip install --quiet --upgrade pyinstaller

set ICON_ARG=
if exist icon.png (
    echo Converting icon.png to icon.ico...
    python -m pip install --quiet --upgrade pillow
    python make_ico.py icon.png icon.ico
    set ICON_ARG=--icon=icon.ico
) else if exist icon.ico (
    set ICON_ARG=--icon=icon.ico
) else (
    echo No icon.png found - using the default PyInstaller icon.
)

python -m PyInstaller --noconfirm --onefile --windowed %ICON_ARG% --name Quizlet2CSV quizlet_gui.py

echo.
echo Built dist\Quizlet2CSV.exe
echo Drag a saved Quizlet HTML file onto it, or double-click it to pick one.
echo.
echo You can close this window now.
pause

endlocal
