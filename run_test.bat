@echo off
cd /d "%~dp0"
echo Running unit tests...
echo.
python test_pulses_unit.py
echo.
pause
