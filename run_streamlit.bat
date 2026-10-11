@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -3 -m venv .venv
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 exit /b 1
if not exist "models\sql_detector.joblib" (
    ".venv\Scripts\python.exe" train_model.py
    if errorlevel 1 exit /b 1
)
".venv\Scripts\python.exe" -m streamlit run streamlit_app.py
pause
