@echo off
echo ============================
echo Building Backend...
echo ============================
cd /d "%~dp0"

REM Удаление build папки
if exist "build" (
    echo Removing build folder...
    rmdir /s /q "build"
)

REM Удаление backend.pyd и вариантов с суффиксом
echo Removing compiled modules...
del /q backend*.pyd 2>nul

REM Сборка
echo Building module...
python setup.py build_ext --inplace

if errorlevel 1 (
    echo Build failed!
    pause
    exit /b
)

echo ============================
echo Build successful!
echo ============================
pause