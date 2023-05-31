ECHO OFF&cls
pyinstaller --onefile --icon=icon64.ico main.py
pyarmor generate --pack dist/main.exe main.py

set /p DUMMY=Hit ENTER to continue...