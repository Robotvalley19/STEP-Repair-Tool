@echo off
REM Wechselt in das Verzeichnis, in dem sich die BAT-Datei befindet
cd /d "%~dp0"

REM Führt app.py mit FreeCAD Python aus
"D:\Program Files\FreeCAD 1.0\bin\python.exe" "%~dp0app.py"

pause
