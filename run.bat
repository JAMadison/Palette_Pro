@echo off
git pull

REM Set up variables
set env_name=venv
set requirements=requirements.txt
set script_name=main.py

REM Check if virtual environment exists
echo Checking for virtual environment...
if exist %env_name% (
    echo Virtual environment found! Activating...
) else (
    echo Virtual environment not found. Creating...
    python -m venv %env_name%
)

REM Activate virtual environment
call %env_name%\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r %requirements%

REM Run script
echo Running Pallet Pro...
python %script_name%

REM Deactivate virtual environment
echo Deactivating virtual environment...
deactivate
