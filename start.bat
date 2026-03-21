@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating venv...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Done! You can now run the project.
pause