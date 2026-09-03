@echo off
cd /d "%~dp0"
if not exist .venv py -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --disable-pip-version-check -q -r requirements.txt
python main.py
