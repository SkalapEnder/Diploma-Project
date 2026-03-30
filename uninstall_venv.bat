@echo off
set VENV_PATH=venv

if exist %VENV_PATH% (
    echo Deleting virtual environment in %VENV_PATH%...
    rmdir /s /q %VENV_PATH%
    echo Done!
) else (
    echo Virtual environment folder "%VENV_PATH%" not found.
)
pause
