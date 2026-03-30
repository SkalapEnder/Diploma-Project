@echo off
title Initialize python project
:: 1. Create virtual environment if not exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment is created!
)

:: 2. Activate and upgrade pip
echo Activate and upgrade pip...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip

setlocal

:: 3. Check if requirements.txt exists
if not exist requirements.txt (
    echo [ERROR] requirements.txt not found! Installation aborted.
    pause
    exit /b 1
)

echo Starting installation from requirements.txt...

:: 4. Run the installation
pip install -r requirements.txt

:: 5. Verification of Error Level
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Installation failed with error code: %errorlevel%
    echo Please check your internet connection or Python version.
    pause
    exit /b %errorlevel%
)

:: 6. Final check for package integrity
echo Verifying installed packages...
pip check
if %errorlevel% neq 0 (
    echo [WARNING] Dependency conflicts detected!
    pause
)

echo [SUCCESS] All libraries installed successfully.
::echo Launch app...
::python src/main.py

pause
