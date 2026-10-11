@echo off
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel%==0 (
    python experiment.py >nul
    start "" http://127.0.0.1:8765
    python app.py
    pause
    exit /b
)
where py >nul 2>nul
if %errorlevel%==0 (
    py -3 experiment.py >nul
    start "" http://127.0.0.1:8765
    py -3 app.py
    pause
    exit /b
)
set "PROJECT_PYTHON=%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
if exist "%PROJECT_PYTHON%" (
    "%PROJECT_PYTHON%" experiment.py >nul
    start "" http://127.0.0.1:8765
    "%PROJECT_PYTHON%" app.py
) else (
    echo Install Python 3.10 or newer, then run this launcher again.
)
pause
