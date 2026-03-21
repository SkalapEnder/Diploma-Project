@echo off
REM Activate virtual environment
call venv\Scripts\activate.bat

REM Generate clean requirements.txt using pipreqs
pip install --upgrade pipreqs
pipreqs . --force

REM Deactivate virtual environment
deactivate

echo requirements.txt updated!
pause