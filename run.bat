@echo off

REM Set up variables
set env_name=venv
set requirements=requirements.txt
set script_name=main.py

REM Activate virtual environment
call %env_name%\Scripts\activate.bat

REM Run script
python %script_name%

REM Deactivate virtual environment
deactivate