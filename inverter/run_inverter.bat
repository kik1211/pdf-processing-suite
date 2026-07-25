@echo off
cd /d "%~dp0"
echo Running PDF inverter...
python invert_all_pdfs.py
pause
