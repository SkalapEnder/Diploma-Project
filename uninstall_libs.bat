@echo off
setlocal
title Uninstalling Project Libraries

:: 0. Activate and upgrade pip
call venv\Scripts\activate.bat

:: 1. Check if requirements.txt exists
if not exist requirements.txt (
    echo [ERROR] requirements.txt not found! Nothing to uninstall.
    pause
    exit /b 1
)

echo [1/2] Starting uninstallation of packages from requirements.txt...

:: 2. Uninstall packages (-y skips confirmation prompts)
pip uninstall -r requirements.txt -y

:: 3. Error level check
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] Some errors occurred during uninstallation.
    echo Please ensure no Python scripts or Qt Designer are currently running.
    pause
    exit /b %errorlevel%
)

:: 4. Optional: Clear pip cache to ensure clean future installs
echo [2/2] Clearing pip download cache...
pip cache purge >nul 2>&1

echo.
echo [SUCCESS] All packages from requirements.txt have been uninstalled.
pause
