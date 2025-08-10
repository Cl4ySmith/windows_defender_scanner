@echo off
chcp 65001 > nul
python "windows_defender_scanner.py" %*
pause
