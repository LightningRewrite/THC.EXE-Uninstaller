@echo off
cd /d "%~dp0"
py -3 thc_exe_uninstaller.py
if errorlevel 1 pause
